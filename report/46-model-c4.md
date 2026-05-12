### 4.6.2. Software Architecture Context Diagram

### 4.6.3. Software Architecture Container Diagrams

### 4.6.4. Software Architecture Components Diagrams
6. Service Execution and Neonatal Monitoring

The Component Diagram of the Service Execution and Neonatal Monitoring bounded context represents the internal structure and interaction between the main components responsible for neonatal monitoring within SIRAN. This diagram illustrates how the system processes clinical information, validates vital signs, detects anomalies, and manages alerts in real time.

The architecture is organized into specialized components that collaborate to ensure continuous monitoring and efficient communication between services. Key components include the Monitoring Controller, Validation Service, Anomaly Detection Engine, Alert Manager, Notification Service, and repositories responsible for data persistence.

This design promotes modularity, scalability, and maintainability by separating responsibilities across independent services. Furthermore, it enables reliable coordination between monitoring processes and alert management, supporting timely medical intervention and improving the overall safety and quality of neonatal care.

<p align="center">
  <img src="assets/Component-diagram-6.png" width="700">
</p>
