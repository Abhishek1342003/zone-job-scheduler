# Part 2 — Cloud, Security & IoT Deployment Blueprint

This blueprint deploys the **exact scheduler, synchronization, deadlock-safety and memory-translation engine from Part 1**. The Part 1 engine is treated as the fixed compute core rather than replaced by another scheduler.

## 9. Distributed architecture and communication plan

### Choice: Hybrid architecture

I choose a **Hybrid** architecture: the three zone controllers operate locally and independently for fast sensor processing, while a central Smart City Operations dashboard provides coordination, monitoring and city-wide visibility. This is preferable to a pure client-server design because the zones can continue local processing during a temporary dashboard outage, while it is more coordinated and operationally manageable than a fully peer-to-peer design.

The choice is based on four criteria:

1. **Fault tolerance:** a failure of the central dashboard should not stop local zone processing. The scheduler and Banker's-Algorithm engine from Part 1 remain available at each zone controller.
2. **Single point of failure:** the dashboard is a coordination/visualization service rather than the only execution point, reducing the effect of central failure.
3. **Scalability:** additional zone controllers can be added without making every controller directly communicate with every other controller.
4. **Transparency:** the dashboard gives Smart City Operations a single view of alerts, controller health and archived sensor information.

### Data flow A — real-time public-safety alert

**Zone controller → dashboard: HTTPS over TCP, synchronous request.**

The zone controller sends an authenticated HTTPS request containing the alert and metadata. TCP provides reliable ordered delivery, while HTTPS provides TLS encryption. This flow is treated as synchronous because the controller needs an acknowledgement that the dashboard service received the alert request; local processing can still continue independently if the central service is temporarily unavailable.

The alert-producing controller runs the **scheduler and Banker's-Algorithm engine from Part 1** for its local workload before publishing the resulting operational event.

### Data flow B — full-day sensor archive

**Zone controller → cloud archive: MQTT over TCP, asynchronous.**

The controller publishes batches of sensor records to an MQTT broker. MQTT's publish/subscribe model is appropriate for telemetry, while TCP gives reliable transport. This flow is asynchronous because a full-day archive does not require an immediate dashboard response and can be buffered and retried when connectivity is interrupted.

The **scheduler and Banker's-Algorithm engine from Part 1** remains the compute core running at the controller; MQTT is only the telemetry transport.

---

## 10. VPC-based network boundary

I use **one VPC with three isolated zone subnets**, one subnet for Zone-A, one for Zone-B and one for Zone-C. Each zone controller is deployed in its own subnet.

The isolation is appropriate because subnet-level separation limits direct east-west reachability and makes zone-specific network policies easier to maintain. A single VPC also gives centralized routing and security-policy management without requiring three independent VPCs.

**Specific boundary control:** VPC **network ACLs (NACLs)** deny direct Zone-A-to-Zone-B traffic while allowing only explicitly required paths through the approved application/gateway route. Security groups additionally restrict inbound controller ports to the required application traffic.

The Smart City Operations dashboard is not named as the enforcement mechanism; the network ACL is the actual network-level boundary control.

---

## 11. Network-security objectives and controls

| Security objective | Specific control/technology | How it protects this platform |
|---|---|---|
| Protect sensitive data | AES-256 encryption at rest | Encrypts sensor archives, JOBS data and operational records stored on controllers/cloud storage. |
| Authentication | Mutual TLS (mTLS) | Controllers and services authenticate each other with certificates before exchanging platform data. |
| Authorization | IAM least-privilege roles | Limits each operator/service to only the APIs and resources required for its job. |
| Prevent cyber attacks | AWS WAF + IDS/IPS monitoring | Filters malicious application traffic and provides detection/response for suspicious network activity. |
| Secure communication | TLS 1.3 / HTTPS | Encrypts public-safety alerts and prevents passive interception or tampering in transit. |
| Ensure availability | Multi-AZ deployment + health checks/autoscaling | Removes dependence on one cloud instance and replaces failed service instances automatically. |

The Part 1 **scheduler and Banker's-Algorithm engine** remains the compute service protected by these controls rather than being replaced by a cloud-native scheduler.

---

## 12. IAM table and data-protection map

### IAM roles

| Role | Permission set |
|---|---|
| Zone Operator | Read/write sensor-ingestion data for the assigned zone; start/stop the Part 1 compute service; view local health; no access to other zones. |
| City Dashboard Admin | Read aggregated alerts/metrics from all zones; manage dashboard configuration; cannot modify controller scheduling data. |
| Auditor | Read-only access to audit logs, IAM events and archived operational records; no write/delete permissions. |
| Archive Service | Write sensor archives and read only the storage location needed for retention verification; no interactive login. |

### Protection by data state

| Data state | Technique | Concrete example |
|---|---|---|
| At rest | AES-256 storage encryption + managed KMS keys | The fixed `JOBS` list and controller results stored on a Zone-A controller/cloud archive are encrypted on disk. |
| In transit | TLS 1.3 / HTTPS or MQTT over TLS | A public-safety alert sent from Zone-B to Smart City Operations is encrypted during transport. |
| In use | Process isolation + least-privilege memory access | The Banker's-Algorithm safety check runs in the protected scheduler process; only the scheduler service account can access its working data. |

---

## 13. IoT connectivity and six-layer architecture

### Devices and communication technologies

| Sensor/device | Technology | Reason |
|---|---|---|
| Traffic-camera trigger | 5G | High bandwidth and low latency support event metadata and selected video/frames where required. |
| Environmental sensor | LoRaWAN | Long range and low power are suitable for distributed temperature/air-quality sensors. |
| Wearable public-safety device | Bluetooth Low Energy (BLE) | Very low power and short-range communication suit a wearable communicating with a nearby gateway. |
| Fixed road-side sensor | NB-IoT | Low-power wide-area connectivity is suitable for fixed telemetry with small payloads. |

### Six IoT architecture layers

| IoT layer | Platform component |
|---|---|
| Physical Environment | Roads, traffic areas, public spaces and environmental conditions monitored by the zones. |
| Perception/Device | Cameras, environmental sensors, wearables and road-side sensors. |
| Gateway | Zone gateway/controller that aggregates device traffic and performs local filtering/processing. |
| Network Communication | 5G, LoRaWAN, BLE and NB-IoT links, followed by IP/TLS connectivity to cloud services. |
| Cloud Platform | **The scheduler and Banker's-Algorithm engine from Part 1** running as the fixed compute core for zone-controller workloads. |
| Application | Smart City Operations dashboard, alert management, analytics and archive access. |

---

## 14. Threats and mitigations

| Threat | Specific mitigation |
|---|---|
| IoT device spoofing / unauthorized device joining | Device certificates with mTLS and certificate-based device enrollment. |
| DDoS against the public-safety dashboard/API | WAF/DDoS protection, rate limiting and autoscaling across multiple availability zones. |
| MQTT interception or credential theft | MQTT over TLS, per-device credentials/certificates and least-privilege topic permissions. |
| Compromised zone controller moving laterally | Network ACL isolation between zone subnets plus restrictive security groups. |
| Ransomware/data destruction in archives | Immutable/versioned backups with restricted write permissions and separate recovery credentials. |

## Deployment summary

The production platform therefore consists of three logically isolated zone controllers, a resilient central operations layer and a cloud archive. Each zone runs the **exact Part 1 scheduler and Banker's-Algorithm engine**, while network controls, IAM, encryption, authenticated communication and IoT security protect the engine and its data.
