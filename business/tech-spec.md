# Tech Spec: Rural Ortho Link v1
## Stack
- **Language**: Node.js (14.x)
- **Framework**: Express.js (4.x)
- **Runtime**: Docker (20.x)
- **Database**: MongoDB (4.x) with Atlas (free-tier)
- **Frontend**: React (17.x) with Next.js (11.x) for static site generation
- **CI/CD**: GitHub Actions (free-tier)

## Hosting
- **Platform**: AWS (free-tier)
- **Region**: us-west-2
- **EC2**: t2.micro instance for development and testing
- **RDS**: MongoDB Atlas (free-tier) for production

## Data Model
- **Collections**:
  - **patients**: stores patient information (e.g., name, email, phone)
    - **_id** (ObjectId): unique patient ID
    - **name** (String): patient name
    - **email** (String): patient email
    - **phone** (String): patient phone number
  - **doctors**: stores doctor information (e.g., name, email, specialty)
    - **_id** (ObjectId): unique doctor ID
    - **name** (String): doctor name
    - **email** (String): doctor email
    - **specialty** (String): doctor specialty
  - **appointments**: stores appointment information (e.g., date, time, patient, doctor)
    - **_id** (ObjectId): unique appointment ID
    - **date** (Date): appointment date
    - **time** (String): appointment time
    - **patient** (ObjectId): reference to patient document
    - **doctor** (ObjectId): reference to doctor document
  - **prescriptions**: stores prescription information (e.g., medication, dosage, patient)
    - **_id** (ObjectId): unique prescription ID
    - **medication** (String): prescribed medication
    - **dosage** (String): prescribed dosage
    - **patient** (ObjectId): reference to patient document

## API Surface
- **Endpoints**:
  - **GET /patients**: retrieve all patients
  - **GET /patients/:id**: retrieve patient by ID
  - **POST /patients**: create new patient
  - **GET /doctors**: retrieve all doctors
  - **GET /doctors/:id**: retrieve doctor by ID
  - **POST /doctors**: create new doctor
  - **GET /appointments**: retrieve all appointments
  - **GET /appointments/:id**: retrieve appointment by ID
  - **POST /appointments**: create new appointment
  - **GET /prescriptions**: retrieve all prescriptions
  - **GET /prescriptions/:id**: retrieve prescription by ID
  - **POST /prescriptions**: create new prescription

## Security Model
- **Auth**: OAuth 2.0 with Google Sign-In
- **Secrets**: stored in AWS Secrets Manager (free-tier)
- **IAM**: AWS IAM roles for EC2 and RDS instances

## Observability
- **Logs**: sent to AWS CloudWatch Logs (free-tier)
- **Metrics**: sent to AWS CloudWatch Metrics (free-tier)
- **Traces**: sent to AWS X-Ray (free-tier)

## Build/CI
- **Build**: Node.js and React applications built using npm scripts
- **CI**: GitHub Actions workflow for automated testing and deployment
- **Deployment**: automated deployment to AWS EC2 instance using GitHub Actions