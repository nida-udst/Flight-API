# Flight API
This project was proposed and developed based on my own idea as an individual final project for the course IT Systems Integration, designed to manage airport flight information, supporting full CRUD operations on flights and gates to allow airport staff to create and manage flights and gates data, ensuring valid and reliable information is stored in the database

Moreover, the flight management system includes automated gate status synchronization based on flight status changes (e.g. Boarding → Departed automatically closes the gate), auto-updates relevant fields such as actual departure time, and enforces strict status transition validations to ensure flights follow a logical lifecycle before any status change is applied.


## Project Structure
```
SourceCode
├── _pycache_/
├── migrations/
├── models/
│      ├── flight.py
│      ├── flight_status.py
│      └── gate.py
│ 
├── resources/
│      ├── flight.py
│      ├── flight_status.py
│      └── gate.py
│ 
├── app.py
├── config.py
├── extensions.py
└── requirements.txt
```
## Flight Status Lifecycle

Flights follow a strict status progression enforced by validation at each transition. A gate assignment is required before any status change can be applied.

| Step | Endpoint | Flight Status | Gate Status | Additional Changes |
|---|---|---|---|---|
| 1 | `PUT /flights/<id>/board` | → `Boarding` | → `Open` | — |
| 2 | `DELETE /flights/<id>/board` | → `Departed` | → `Closed` | Actual departure time set |
| 3 | `PUT /flights/<id>/airborne` | → `In Flight` | → `Available` | Gate freed for other flights |
| 4 | `DELETE /flights/<id>/airborne` | → `Arrived` | Gate unassigned (`null`) | Actual arrival time set |

**Validations:**
- A flight **must have a gate assigned** before it can be set to `Boarding`
- A flight **must be** `Boarding` before it can be set to `Departed`
- A flight **must be** `Departed` before it can be set to `In Flight`
- A flight **must be** `In Flight` before it can be set to `Arrived`
- Each transition is validated against the **previous status**, preventing any out-of-order or illegal state changes

### Kindly review the project report for further details regarding the API endpoints, ER Model, and Endpoints Testing.
