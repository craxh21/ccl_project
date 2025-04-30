# ☁️ Cloud-Based File Handling with Duplication Removal using MD5

A cloud-native file upload system that intelligently detects and prevents duplicate files using MD5 checksum, storing only unique files in AWS S3 while tracking metadata in MongoDB Atlas.

<!--*(Consider adding an actual architecture diagram here)*-->

## 🚀 Key Features
- **Smart Duplicate Detection** - MD5 checksum prevents redundant file storage
- **Efficient Cloud Storage** - Only unique files stored in AWS S3
- **Comprehensive Metadata Tracking** - File details stored in MongoDB Atlas
- **Scalable Deployment** - Hosted on AWS EC2 for elastic scaling
- **Simple API Interface** - Easy file uploads via Flask REST API

## 🛠️ Technology Stack
| Category        | Technology           |
|-----------------|----------------------|
| Backend        | Python 3, Flask      |
| Database       | MongoDB Atlas        |
| Cloud Storage  | AWS S3               |
| Deployment     | AWS EC2 (Ubuntu)     |
| Libraries      | boto3, pymongo, dotenv |

## 📂 System Architecture
1. User uploads file via Flask API endpoint
2. System computes MD5 checksum of file
3. Checks MongoDB for existing checksum:
   - **Exists** → Skip S3 upload, update access timestamp
   - **New File** → Upload to S3, store metadata in MongoDB
4. Files stored only once, optimizing storage costs

```mermaid
graph TD
    A[User Upload] --> B[Compute MD5]
    B --> C{Check MongoDB}
    C -->|Exists| D[Update Metadata]
    C -->|New| E[Upload to S3]
    E --> F[Store Metadata]
