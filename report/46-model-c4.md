### 4.6.2. Software Architecture Context Diagram

6. Service Execution and Neonatal Monitoring

The Context Diagram of the Service Execution and Neonatal Monitoring bounded context provides a high-level view of how SIRAN interacts with its primary users and external actors. This diagram illustrates the relationship between the neonatal monitoring platform and the stakeholders involved in the monitoring process, including parents and pediatricians.

The context view highlights how users interact with the system to register neonatal health information, review alerts, and access monitoring reports. It also demonstrates the role of SIRAN as a centralized platform that supports communication, supervision, and decision-making in neonatal care.

This representation helps define the system boundaries and clarifies the interactions between external actors and the monitoring ecosystem, ensuring a better understanding of the platform’s operational environment and responsibilities.

<p align="center">
  <img src="assets/Context-diagram-6.png" width="700">
</p>

### 4.6.3. Software Architecture Container Diagrams

6. Service Execution and Neonatal Monitoring

The Container Diagram of the Service Execution and Neonatal Monitoring bounded context describes the main technological containers that compose the SIRAN platform and the interactions between them. This diagram illustrates how the frontend application, backend services, and database collaborate to support neonatal monitoring operations.

The architecture is divided into independent containers, including the Web Application developed with Vue.js, the Monitoring API implemented with Spring Boot, and the Monitoring Database responsible for storing clinical information and alerts. These containers communicate through RESTful interactions, enabling efficient processing and real-time access to neonatal monitoring data.

This design promotes scalability, separation of concerns, and maintainability by organizing the system into clearly defined layers. Additionally, it ensures a reliable flow of information between users, services, and data storage, supporting continuous monitoring and timely medical response within the SIRAN ecosystem.

<p align="center">
  <img src="assets/Container-diagram-6.png" width="700">
</p>

### 4.6.4. Software Architecture Components Diagrams

6. Service Execution and Neonatal Monitoring

The Component Diagram of the Service Execution and Neonatal Monitoring bounded context represents the internal structure and interaction between the main components responsible for neonatal monitoring within SIRAN. This diagram illustrates how the system processes clinical information, validates vital signs, detects anomalies, and manages alerts in real time.

The architecture is organized into specialized components that collaborate to ensure continuous monitoring and efficient communication between services. Key components include the Monitoring Controller, Validation Service, Anomaly Detection Engine, Alert Manager, Notification Service, and repositories responsible for data persistence.

This design promotes modularity, scalability, and maintainability by separating responsibilities across independent services. Furthermore, it enables reliable coordination between monitoring processes and alert management, supporting timely medical intervention and improving the overall safety and quality of neonatal care.

<p align="center">
  <img src="assets/Component-diagram-6.png" width="700">
</p>
