/*
 * ns-3 port of QLFR (Zhou, Cao, Xiang, IEEE IoTJ 2021) and LAQR (ours) over the ns-3 UAN stack.
 *
 * Stack: UanPhyGen (BPSK, UanPhyPerCommonModes, SINR with interference) + UanPropModelThorp +
 *        UanNoiseModelDefault + UanMacAloha (no carrier sense: collisions are modelled) +
 *        AcousticModemEnergyModel / BasicEnergySource.
 * Routing (this file): round-based, as in the Python reference (qlfr_repro/uwsim/paper_sim.py):
 *   - every round nodes move (3-D random walk, sources fixed at the bottom, sinks fixed at the surface),
 *     broadcast a hello beacon (V, depth, residual energy, tx sequence number), then each sensor runs one
 *     Q-update (QLFR Eq. 8) and the sources send one data packet each;
 *   - data forwarding: priority list of shallower neighbours by Q, holding time tau(n) = k (n - 1),
 *     overhearing suppression (QLFR Alg. 1);
 *   - QLFR: global list length adapted from sink PDR vs P_th (QLFR Sec. IV-D);
 *   - LAQR: link quality p_hat from tx-sequence gaps (EWMA, beta), reward - w_lq (1 - p_hat),
 *     per-hop list length = smallest L with 1 - prod(1 - p_hat) >= rho.
 * Output: one CSV line of metrics on stdout.
 */
#include "ns3/core-module.h"
#include "ns3/energy-module.h"
#include "ns3/mobility-module.h"
#include "ns3/network-module.h"
#include "ns3/uan-module.h"

#include <algorithm>
#include <cmath>
#include <cstring>
#include <iostream>
#include <map>
#include <random>
#include <set>
#include <vector>

using namespace ns3;

// ------------------------------------------------------------------------------------------ header
class LaqrHeader : public Header
{
  public:
    uint8_t type{0}; // 0 = hello, 1 = data
    uint32_t src{0}, pktId{0}, sender{0}, txseq{0};
    float v{0}, depth{0}, energy{0};
    std::vector<uint32_t> plist;

    static TypeId GetTypeId()
    {
        static TypeId tid = TypeId("LaqrHeader").SetParent<Header>().AddConstructor<LaqrHeader>();
        return tid;
    }

    TypeId GetInstanceTypeId() const override
    {
        return GetTypeId();
    }

    uint32_t GetSerializedSize() const override
    {
        return 1 + 4 * 4 + 3 * 4 + 1 + 4 * plist.size();
    }

    static uint32_t F2U(float f)
    {
        uint32_t u;
        std::memcpy(&u, &f, 4);
        return u;
    }

    static float U2F(uint32_t u)
    {
        float f;
        std::memcpy(&f, &u, 4);
        return f;
    }

    void Serialize(Buffer::Iterator i) const override
    {
        i.WriteU8(type);
        i.WriteHtonU32(src);
        i.WriteHtonU32(pktId);
        i.WriteHtonU32(sender);
        i.WriteHtonU32(txseq);
        i.WriteHtonU32(F2U(v));
        i.WriteHtonU32(F2U(depth));
        i.WriteHtonU32(F2U(energy));
        i.WriteU8(static_cast<uint8_t>(plist.size()));
        for (auto id : plist)
        {
            i.WriteHtonU32(id);
        }
    }

    uint32_t Deserialize(Buffer::Iterator i) override
    {
        type = i.ReadU8();
        src = i.ReadNtohU32();
        pktId = i.ReadNtohU32();
        sender = i.ReadNtohU32();
        txseq = i.ReadNtohU32();
        v = U2F(i.ReadNtohU32());
        depth = U2F(i.ReadNtohU32());
        energy = U2F(i.ReadNtohU32());
        uint8_t n = i.ReadU8();
        plist.resize(n);
        for (auto& id : plist)
        {
            id = i.ReadNtohU32();
        }
        return GetSerializedSize();
    }

    void Print(std::ostream& os) const override
    {
        os << "type=" << int(type) << " src=" << src << " pkt=" << pktId << " sender=" << sender;
    }
};

// ------------------------------------------------------------------------------------------ params
struct Params
{
    std::string protocol{"qlfr"}; // qlfr | laqr
    uint32_t nSensors{100}, nSources{5}, nSinks{5}, rounds{50}, seed{1};
    double area{500}, R{150}, speed{3}, roundS{10}, helloWindow{6.0}, dataJitter{3.5}, k{0.15};
    uint32_t freshRounds{1}, helloEvery{1};
    double gamma{0.8}, alpha{0.5}, eIni{1000}, psiT{2}, psiR{0.5};
    double pdrTh{0.90};
    uint32_t listLen0{3}, listLenMax{8};
    double beta{0.05}, rho{0.99}, wLq{0.25}, prior{0.9};
    bool resetP{true};
    bool ackLearn{false}; // superseded by ackMode, kept for CLI compatibility
    double ackWait{1.0}, ackBeta{0.1};
    int ackMode{0};
    uint32_t dataBytes{63}, helloBytes{30}; // data ~ 500 bits as in the Python model; hello = header only
    double txPowerDb{114}, rxThreshDb{10}; // 114 dB re uPa at 40 kHz: link cutoff 150-175 m (calibrated)
    double fcHz{40000}, bwHz{20000}, rateBps{20000};
};

struct Nbr
{
    double V{0}, depth{0}, energy{0};
    uint32_t lastRound{0};
    double p{0.9};
    int64_t lastSeq{-1};
};

struct NodeState
{
    bool sink{false};
    Ptr<UanNetDevice> dev;
    Ptr<ConstantPositionMobilityModel> mob;
    Ptr<energy::BasicEnergySource> src;
    uint32_t txseq{0};
    double V{0};
    std::map<uint32_t, Nbr> nbr;
    std::map<uint32_t, double> Q;
    std::set<uint64_t> forwarded;
    std::map<uint64_t, EventId> held;
    double ackRate{1.0}, headRate{1.0}; // node-level EWMA: observed vs predicted top-candidate success
    std::set<std::pair<uint64_t, uint32_t>> heardFwd; // (packet, forwarder) overheard by this node
};

// ------------------------------------------------------------------------------------------ simulation
class LaqrSim
{
  public:
    explicit LaqrSim(const Params& p)
        : P(p),
          rng(p.seed * 7919u + 13u)
    {
    }

    void Build();
    void Run();
    void Report() const;

  private:
    Params P;
    std::mt19937 rng;
    NodeContainer nodes;
    std::vector<NodeState> S;
    std::map<Ptr<NetDevice>, uint32_t> devIndex;
    uint32_t round{0}, listLen{3};
    double headOut{0}, listSum{0}, headDist{0}, candDist{0}, headP{0};
    uint32_t gen{0}, dataTx{0}, helloTx{0}, sendFails{0}, helloRx{0}, dataRx{0}, candRx{0}, voidDrops{0};
    std::map<uint64_t, double> t0, delivered;

    double Depth(uint32_t i) const
    {
        return S[i].mob->GetPosition().z;
    }

    double Energy(uint32_t i) const
    {
        return S[i].sink ? P.eIni : S[i].src->GetRemainingEnergy();
    }

    double Ce(double e) const
    {
        return 1.0 - e / P.eIni;
    }

    bool Fresh(const Nbr& n) const
    {
        return n.lastRound + P.freshRounds > round; // heard within the last freshRounds rounds
    }

    double U()
    {
        return std::uniform_real_distribution<double>(0, 1)(rng);
    }

    void StartRound();
    void Move();
    void SendHello(uint32_t i);
    void UpdateQ();
    void GenerateData();
    void EndRound();
    std::vector<uint32_t> PriorityList(uint32_t i);
    void SendData(uint32_t i, uint32_t src, uint32_t pktId);
    void Transmit(uint32_t i, Ptr<Packet> pkt, uint32_t attempt, bool isData);
    void Fire(uint32_t j, uint64_t key);
    bool Receive(Ptr<NetDevice> dev, Ptr<const Packet> pkt, uint16_t proto, const Address& from);
    void LearnLink(Nbr& n, double ok);
    void CheckAck(uint32_t i, uint64_t key, uint32_t j0);
    uint32_t ackOk{0}, ackFail{0};
};

void
LaqrSim::Build()
{
    listLen = P.listLen0;
    uint32_t N = P.nSensors + P.nSinks;
    nodes.Create(N);
    S.resize(N);

    MobilityHelper mh;
    mh.SetMobilityModel("ns3::ConstantPositionMobilityModel");
    mh.Install(nodes);
    std::uniform_real_distribution<double> ux(0, P.area);
    for (uint32_t i = 0; i < N; ++i)
    {
        S[i].sink = i >= P.nSensors;
        S[i].mob = nodes.Get(i)->GetObject<ConstantPositionMobilityModel>();
        double z = S[i].sink ? 0.0 : (i < P.nSources ? P.area : ux(rng));
        S[i].mob->SetPosition(Vector(ux(rng), ux(rng), z));
    }

    UanTxMode mode = UanTxModeFactory::CreateMode(UanTxMode::PSK, P.rateBps, P.rateBps, P.fcHz, P.bwHz, 2,
                                                  "BPSK");
    UanModesList modes;
    modes.AppendMode(mode);
    UanHelper uan;
    uan.SetPhy("ns3::UanPhyGen", "PerModel", StringValue("ns3::UanPhyPerCommonModes"), "SupportedModes",
               UanModesListValue(modes), "TxPower", DoubleValue(P.txPowerDb), "RxThreshold",
               DoubleValue(P.rxThreshDb));
    uan.SetMac("ns3::UanMacAloha");
    Ptr<UanChannel> ch = CreateObject<UanChannel>();
    ch->SetPropagationModel(CreateObject<UanPropModelThorp>());
    ch->SetNoiseModel(CreateObject<UanNoiseModelDefault>());
    NetDeviceContainer devs = uan.Install(nodes, ch);

    BasicEnergySourceHelper esh;
    esh.Set("BasicEnergySourceInitialEnergyJ", DoubleValue(P.eIni));
    energy::EnergySourceContainer sources = esh.Install(nodes);
    AcousticModemEnergyModelHelper emh;
    emh.Set("TxPowerW", DoubleValue(P.psiT));
    emh.Set("RxPowerW", DoubleValue(P.psiR));
    emh.Set("IdlePowerW", DoubleValue(0.0));
    emh.Set("SleepPowerW", DoubleValue(0.0));
    emh.Install(devs, sources);

    for (uint32_t i = 0; i < N; ++i)
    {
        S[i].dev = DynamicCast<UanNetDevice>(devs.Get(i));
        S[i].src = DynamicCast<energy::BasicEnergySource>(sources.Get(i));
        devIndex[devs.Get(i)] = i;
        devs.Get(i)->SetReceiveCallback(MakeCallback(&LaqrSim::Receive, this));
    }
}

void
LaqrSim::Run()
{
    for (uint32_t r = 0; r < P.rounds; ++r)
    {
        Simulator::Schedule(Seconds(r * P.roundS), &LaqrSim::StartRound, this);
        Simulator::Schedule(Seconds(r * P.roundS + P.helloWindow), &LaqrSim::UpdateQ, this);
        Simulator::Schedule(Seconds(r * P.roundS + P.helloWindow + 0.1), &LaqrSim::GenerateData, this);
        Simulator::Schedule(Seconds((r + 1) * P.roundS - 1e-3), &LaqrSim::EndRound, this);
    }
    Simulator::Stop(Seconds(P.rounds * P.roundS));
    Simulator::Run();
}

void
LaqrSim::StartRound()
{
    round = static_cast<uint32_t>(std::lround(Simulator::Now().GetSeconds() / P.roundS));
    if (round > 0)
    {
        Move();
    }
    for (uint32_t i = 0; i < S.size(); ++i)
    {
        if ((round + i) % P.helloEvery == 0) // each node beacons once every helloEvery rounds
        {
            Simulator::Schedule(Seconds(U() * (P.helloWindow - 0.2)), &LaqrSim::SendHello, this, i);
        }
    }
}

void
LaqrSim::Move()
{
    std::normal_distribution<double> g(0, 1);
    double step = P.speed * P.roundS;
    for (uint32_t i = 0; i < S.size(); ++i)
    {
        if (S[i].sink)
        {
            continue;
        }
        Vector p = S[i].mob->GetPosition();
        double dx = g(rng), dy = g(rng), dz = g(rng);
        double n = std::sqrt(dx * dx + dy * dy + dz * dz);
        double c[3] = {p.x + step * dx / n, p.y + step * dy / n, p.z + step * dz / n};
        for (double& v : c)
        {
            v = std::fabs(v);
            v = P.area - std::fabs(P.area - v); // reflect at the walls
        }
        if (i < P.nSources)
        {
            c[2] = P.area; // sources stay at the bottom layer
        }
        S[i].mob->SetPosition(Vector(c[0], c[1], c[2]));
    }
}

void
LaqrSim::SendHello(uint32_t i)
{
    helloTx++;
    Transmit(i, Create<Packet>(P.helloBytes - LaqrHeader().GetSerializedSize()), 0, false); // header added in Transmit
}

void
LaqrSim::Transmit(uint32_t i, Ptr<Packet> pkt, uint32_t attempt, bool isData)
{
    // Hellos arrive without a LaqrHeader; data packets carry one. Either way the header is (re)written
    // here so that it holds the current tx sequence number, V, depth and residual energy.
    LaqrHeader h;
    Ptr<Packet> body = pkt->Copy();
    if (isData)
    {
        body->RemoveHeader(h);
    }
    else
    {
        h.type = 0;
        h.sender = i;
    }
    h.v = S[i].V;
    h.depth = Depth(i);
    h.energy = Energy(i);
    h.txseq = S[i].txseq + 1;
    Ptr<Packet> out = body->Copy();
    out->AddHeader(h);
    if (S[i].dev->Send(out, S[i].dev->GetBroadcast(), 0))
    {
        S[i].txseq++;
        return;
    }
    sendFails++; // PHY busy transmitting (half duplex): retry after one packet time
    if (attempt < 20)
    {
        Simulator::Schedule(Seconds(P.dataBytes * 8.0 / P.rateBps + 1e-3), &LaqrSim::Transmit, this, i, pkt,
                            attempt + 1, isData);
    }
}

void
LaqrSim::LearnLink(Nbr& n, double ok)
{
    n.p += P.beta * (ok - n.p);
}

void
LaqrSim::UpdateQ()
{
    bool laqr = P.protocol == "laqr";
    std::vector<double> newV(S.size());
    for (uint32_t i = 0; i < S.size(); ++i)
    {
        newV[i] = S[i].V;
        if (S[i].sink)
        {
            newV[i] = 0;
            continue;
        }
        double ei = Energy(i), di = Depth(i);
        double best = -1e18;
        bool any = false;
        for (auto& [j, n] : S[i].nbr)
        {
            if (!Fresh(n))
            {
                continue;
            }
            double cd = 0.5 * (1.0 - (di - n.depth) / P.R);                       // Eq. (7)
            double r = -Ce(ei) - (S[j].sink ? 0.0 : Ce(n.energy)) - cd;           // Eq. (5)-(6)
            if (laqr)
            {
                r -= P.wLq * (1.0 - n.p);
            }
            double& q = S[i].Q[j];
            q = P.alpha * (r + P.gamma * n.V) + (1 - P.alpha) * q;                 // Eq. (8)
            best = std::max(best, q);
            any = true;
        }
        if (any)
        {
            newV[i] = best;
        }
    }
    for (uint32_t i = 0; i < S.size(); ++i)
    {
        S[i].V = newV[i];
    }
}

std::vector<uint32_t>
LaqrSim::PriorityList(uint32_t i)
{
    double di = Depth(i);
    std::vector<std::pair<double, uint32_t>> c;
    for (auto& [j, n] : S[i].nbr)
    {
        if (Fresh(n) && n.depth < di)
        {
            c.emplace_back(S[i].Q.count(j) ? S[i].Q[j] : 0.0, j);
        }
    }
    std::sort(c.begin(), c.end(), [](auto& a, auto& b) { return a.first > b.first; });
    std::vector<uint32_t> out;
    if (P.protocol == "laqr")
    {
        double miss = 1.0;
        for (auto& [q, j] : c)
        {
            out.push_back(j);
            double pj = std::clamp(S[i].nbr[j].p, 0.0, 1.0);
            if (P.ackMode == 2) // scale beacon-based estimates by the observed/predicted data-plane success
            {
                pj *= std::min(1.0, S[i].ackRate / std::max(1e-3, S[i].headRate));
            }
            miss *= 1.0 - pj;
            if (1.0 - miss >= P.rho || out.size() >= P.listLenMax)
            {
                break;
            }
        }
    }
    else
    {
        for (uint32_t n = 0; n < c.size() && n < listLen; ++n)
        {
            out.push_back(c[n].second);
        }
    }
    return out;
}

void
LaqrSim::GenerateData()
{
    for (uint32_t s = 0; s < P.nSources; ++s)
    {
        uint32_t id = gen++;
        uint64_t key = (uint64_t(s) << 32) | id;
        double jitter = U() * P.dataJitter;              // de-synchronise the sources (ALOHA MAC)
        t0[key] = Simulator::Now().GetSeconds() + jitter;
        S[s].forwarded.insert(key);
        Simulator::Schedule(Seconds(jitter), &LaqrSim::SendData, this, s, s, id);
    }
}

void
LaqrSim::SendData(uint32_t i, uint32_t src, uint32_t pktId)
{
    LaqrHeader h;
    h.type = 1;
    h.src = src;
    h.pktId = pktId;
    h.sender = i;
    h.v = S[i].V;
    h.depth = Depth(i);
    h.energy = Energy(i);
    h.plist = PriorityList(i);
    if (h.plist.empty())
    {
        voidDrops++;
        if (getenv("LAQR_DEBUG"))
        {
            uint32_t fresh = 0, shallow = 0;
            for (auto& [j, n] : S[i].nbr)
            {
                fresh += Fresh(n);
                shallow += Fresh(n) && n.depth < Depth(i);
            }
            std::cerr << "void node=" << i << " round=" << round << " depth=" << Depth(i)
                      << " nbrs=" << S[i].nbr.size() << " fresh=" << fresh << " shallow=" << shallow << std::endl;
        }
        return; // void: no shallower neighbour
    }
    listSum += h.plist.size();
    headDist += CalculateDistance(S[i].mob->GetPosition(), S[h.plist[0]].mob->GetPosition());
    headOut += CalculateDistance(S[i].mob->GetPosition(), S[h.plist[0]].mob->GetPosition()) > 160;
    headP += S[i].nbr[h.plist[0]].p;
    uint32_t pay = P.dataBytes > h.GetSerializedSize() ? P.dataBytes - h.GetSerializedSize() : 0;
    Ptr<Packet> pkt = Create<Packet>(pay);
    pkt->AddHeader(h);
    dataTx++;
    Transmit(i, pkt, 0, true);
    if (P.ackLearn && P.ackMode == 0)
    {
        P.ackMode = 1;
    }
    if (P.ackMode > 0 && P.protocol == "laqr" && !S[h.plist[0]].sink)
    {
        // The top-ranked candidate has holding time 0 and is never suppressed, so whether it forwards
        // is an unbiased (or, if the reverse link also fails, conservative) sample of this link.
        uint64_t key = (uint64_t(src) << 32) | pktId;
        Simulator::Schedule(Seconds(P.ackWait), &LaqrSim::CheckAck, this, i, key, h.plist[0]);
    }
}

bool
LaqrSim::Receive(Ptr<NetDevice> dev, Ptr<const Packet> p, uint16_t, const Address&)
{
    uint32_t j = devIndex[dev];
    Ptr<Packet> pkt = p->Copy();
    LaqrHeader h;
    pkt->RemoveHeader(h);
    uint32_t s = h.sender;
    // routing knowledge exchange (QLFR Sec. V-B) and link learning (LAQR)
    Nbr& n = S[j].nbr[s];
    if (n.lastRound + P.freshRounds <= round)
    {
        n.lastSeq = -1; // neighbour timed out: do not count the absence as sequence gaps
        if (P.resetP)
        {
            n.p = P.prior;
        }
    }
    if (n.lastSeq >= 0)
    {
        int64_t gap = int64_t(h.txseq) - n.lastSeq - 1;
        for (int64_t g = 0; g < std::min<int64_t>(gap, 5); ++g)
        {
            LearnLink(n, 0.0);
        }
    }
    LearnLink(n, 1.0);
    n.lastSeq = h.txseq;
    n.V = h.v;
    n.depth = h.depth;
    n.energy = h.energy;
    n.lastRound = round;
    if (h.type != 1)
    {
        helloRx++;
        return true;
    }
    dataRx++;
    uint64_t key = (uint64_t(h.src) << 32) | h.pktId;
    if (P.ackMode > 0)
    {
        S[j].heardFwd.insert({key, s});
    }
    auto it = S[j].held.find(key);
    if (it != S[j].held.end())
    {
        it->second.Cancel(); // overheard during holding time (Alg. 1, lines 12-13)
        S[j].held.erase(it);
    }
    if (S[j].sink)
    {
        if (!delivered.count(key))
        {
            delivered[key] = Simulator::Now().GetSeconds() - t0[key];
        }
        return true;
    }
    if (S[j].forwarded.count(key))
    {
        return true;
    }
    auto pos = std::find(h.plist.begin(), h.plist.end(), j);
    if (pos == h.plist.end())
    {
        return true; // not a candidate (Alg. 1, lines 4-5)
    }
    candRx++;
    candDist += CalculateDistance(S[j].mob->GetPosition(), S[s].mob->GetPosition());
    double tau = P.k * double(pos - h.plist.begin()); // Eq. (15)
    S[j].held[key] = Simulator::Schedule(Seconds(tau), &LaqrSim::Fire, this, j, key);
    return true;
}

void
LaqrSim::CheckAck(uint32_t i, uint64_t key, uint32_t j0)
{
    bool ok = S[i].heardFwd.count({key, j0}) > 0;
    (ok ? ackOk : ackFail)++;
    if (P.ackMode == 1)
    {
        LearnLink(S[i].nbr[j0], ok ? 1.0 : 0.0);
        return;
    }
    S[i].ackRate += P.ackBeta * ((ok ? 1.0 : 0.0) - S[i].ackRate);
    S[i].headRate += P.ackBeta * (std::clamp(S[i].nbr[j0].p, 0.0, 1.0) - S[i].headRate);
}

void
LaqrSim::Fire(uint32_t j, uint64_t key)
{
    S[j].held.erase(key);
    if (S[j].forwarded.count(key))
    {
        return;
    }
    S[j].forwarded.insert(key);
    SendData(j, uint32_t(key >> 32), uint32_t(key & 0xffffffffu));
}

void
LaqrSim::EndRound()
{
    for (auto& s : S)
    {
        s.heardFwd.clear();
        for (auto& [k, e] : s.held)
        {
            e.Cancel();
        }
        s.held.clear();
    }
    double pdr = gen ? double(delivered.size()) / gen : 0;
    if (pdr > P.pdrTh) // QLFR multipath suppression (Sec. IV-D)
    {
        listLen = std::max<uint32_t>(1, listLen - 1);
    }
    else
    {
        listLen = std::min<uint32_t>(P.listLenMax, listLen + 1);
    }
}

void
LaqrSim::Report() const
{
    double used = 0, minLife = 1e30, T = P.rounds * P.roundS;
    for (uint32_t i = 0; i < S.size(); ++i)
    {
        if (S[i].sink)
        {
            continue;
        }
        double u = P.eIni - S[i].src->GetRemainingEnergy();
        used += u;
        minLife = std::min(minLife, P.eIni * T / std::max(u, 1e-12));
    }
    double delay = 0;
    for (auto& [k, d] : delivered)
    {
        delay += d;
    }
    std::cout << P.protocol << "," << P.nSensors << "," << P.seed << "," << P.speed << ","
              << (gen ? double(delivered.size()) / gen : 0) << ","
              << (delivered.empty() ? NAN : delay / delivered.size()) << "," << used << "," << minLife << ","
              << double(dataTx) / std::max(gen, 1u) << "," << helloTx << "," << sendFails << std::endl;
    std::cerr << "debug helloRx=" << helloRx << " dataRx=" << dataRx << " candRx=" << candRx
              << " voidDrops=" << voidDrops << " gen=" << gen << " meanList=" << listSum / std::max(1u, dataTx)
              << " headDist=" << headDist / std::max(1u, dataTx) << " headP=" << headP / std::max(1u, dataTx)
              << " candDist=" << candDist / std::max(1u, candRx) << " headOut=" << headOut / std::max(1u, dataTx) << " ackOk=" << ackOk << " ackFail=" << ackFail << std::endl;
}

// ------------------------------------------------------------------------------------------ calibration
static void
Calibrate(Params P)
{
    // two nodes; node 0 sends 400 packets to broadcast at distance d; count receptions at node 1
    for (double d : {50.0, 100.0, 125.0, 150.0, 175.0, 200.0, 250.0})
    {
        NodeContainer nc;
        nc.Create(2);
        MobilityHelper mh;
        mh.SetMobilityModel("ns3::ConstantPositionMobilityModel");
        mh.Install(nc);
        nc.Get(0)->GetObject<MobilityModel>()->SetPosition(Vector(0, 0, 100));
        nc.Get(1)->GetObject<MobilityModel>()->SetPosition(Vector(d, 0, 100));
        UanTxMode mode = UanTxModeFactory::CreateMode(UanTxMode::PSK, P.rateBps, P.rateBps, P.fcHz, P.bwHz, 2,
                                                      "BPSK");
        UanModesList modes;
        modes.AppendMode(mode);
        UanHelper uan;
        uan.SetPhy("ns3::UanPhyGen", "PerModel", StringValue("ns3::UanPhyPerCommonModes"), "SupportedModes",
                   UanModesListValue(modes), "TxPower", DoubleValue(P.txPowerDb), "RxThreshold",
                   DoubleValue(P.rxThreshDb));
        uan.SetMac("ns3::UanMacAloha");
        Ptr<UanChannel> ch = CreateObject<UanChannel>();
        ch->SetPropagationModel(CreateObject<UanPropModelThorp>());
        ch->SetNoiseModel(CreateObject<UanNoiseModelDefault>());
        NetDeviceContainer devs = uan.Install(nc, ch);
        uint32_t rx = 0;
        devs.Get(1)->SetReceiveCallback(NetDevice::ReceiveCallback(
            [&rx](Ptr<NetDevice>, Ptr<const Packet>, uint16_t, const Address&) {
                rx++;
                return true;
            }));
        for (uint32_t t = 0; t < 400; ++t)
        {
            Simulator::Schedule(Seconds(t * 0.5), [&devs, &P]() {
                devs.Get(0)->Send(Create<Packet>(P.dataBytes), devs.Get(0)->GetBroadcast(), 0);
            });
        }
        Simulator::Run();
        Simulator::Destroy();
        std::cout << "calib," << P.txPowerDb << "," << d << "," << rx / 400.0 << std::endl;
    }
}

int
main(int argc, char* argv[])
{
    Params P;
    bool calib = false;
    CommandLine cmd(__FILE__);
    cmd.AddValue("protocol", "qlfr | laqr", P.protocol);
    cmd.AddValue("nodes", "number of sensor nodes", P.nSensors);
    cmd.AddValue("rounds", "packet rounds", P.rounds);
    cmd.AddValue("seed", "random seed / run", P.seed);
    cmd.AddValue("speed", "random-walk speed (m/s)", P.speed);
    cmd.AddValue("dataJitter", "max per-source data start jitter (s)", P.dataJitter);
    cmd.AddValue("roundS", "round length (s)", P.roundS);
    cmd.AddValue("k", "holding-time step (s)", P.k);
    cmd.AddValue("pdrTh", "QLFR multipath-suppression threshold", P.pdrTh);
    cmd.AddValue("beta", "LAQR link EWMA rate", P.beta);
    cmd.AddValue("rho", "LAQR per-hop reliability target", P.rho);
    cmd.AddValue("wLq", "LAQR link-quality weight", P.wLq);
    cmd.AddValue("prior", "LAQR prior link success", P.prior);
    cmd.AddValue("ackLearn", "LAQR: also learn p_hat from overhearing the top candidate forward", P.ackLearn);
    cmd.AddValue("ackMode", "0 off, 1 per-link samples, 2 node-level calibration of p_hat", P.ackMode);
    cmd.AddValue("ackBeta", "EWMA rate of the node-level calibration", P.ackBeta);
    cmd.AddValue("ackWait", "time to wait for the top candidate's forward (s)", P.ackWait);
    cmd.AddValue("resetP", "reset p_hat when a neighbour times out", P.resetP);
    cmd.AddValue("txPowerDb", "UanPhyGen TxPower (dB re uPa)", P.txPowerDb);
    cmd.AddValue("helloWindow", "hello beacon window per round (s)", P.helloWindow);
    cmd.AddValue("freshRounds", "neighbour entry lifetime (rounds)", P.freshRounds);
    cmd.AddValue("helloEvery", "beacon period (rounds)", P.helloEvery);
    cmd.AddValue("rateBps", "modem bit rate (bit/s)", P.rateBps);
    cmd.AddValue("fcHz", "carrier frequency (Hz)", P.fcHz);
    cmd.AddValue("bwHz", "bandwidth (Hz)", P.bwHz);
    cmd.AddValue("calib", "run link calibration instead", calib);
    cmd.Parse(argc, argv);
    RngSeedManager::SetSeed(1);
    RngSeedManager::SetRun(P.seed);
    if (calib)
    {
        Calibrate(P);
        return 0;
    }
    LaqrSim sim(P);
    sim.Build();
    sim.Run();
    sim.Report();
    Simulator::Destroy();
    return 0;
}
