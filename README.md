# CodeFlowOps Test Applications

This repository contains test applications for validating CodeFlowOps deployment capabilities across different technology stacks.

## 🎯 Purpose

Test CodeFlowOps SaaS platform's ability to:
- Detect various technology stacks automatically
- Generate appropriate infrastructure configurations
- Deploy applications to cloud providers
- Monitor and manage deployments

## 📁 Test Applications

### 1. React Frontend (`/test-apps/react-frontend/`)
- **Stack**: React 18, React Router, Axios
- **Purpose**: Test frontend deployment and static asset handling
- **Features**: SPA routing, API integration, responsive design
- **Build**: `npm run build` → static files in `/build`

### 2. FastAPI Backend (`/test-apps/fastapi-backend/`)
- **Stack**: FastAPI, SQLAlchemy, JWT authentication
- **Purpose**: Test API deployment and database integration
- **Features**: REST API, authentication, health checks, analytics
- **Deployment**: Containerized with Dockerfile

### 3. Full-Stack Application (Coming Soon)
- **Frontend**: Next.js with API routes
- **Backend**: Node.js Express or FastAPI
- **Database**: PostgreSQL
- **Purpose**: Test complex multi-service deployments

## 🚀 Testing Scenarios

### Scenario 1: Stack Detection
1. Connect repository to CodeFlowOps
2. Verify detection of:
   - React frontend with package.json
   - FastAPI backend with requirements.txt
   - Build scripts and deployment requirements
   - Environment variable needs

### Scenario 2: Infrastructure Generation
1. Generate Terraform configurations
2. Verify creation of:
   - Static hosting for React (S3, CloudFront)
   - Container deployment for FastAPI (ECS, Lambda)
   - Database setup (RDS) if needed
   - Load balancers and SSL certificates

### Scenario 3: Deployment Testing
1. Deploy applications using CodeFlowOps
2. Verify:
   - Successful builds and deployments
   - Application accessibility
   - SSL certificate installation
   - Environment variable injection

### Scenario 4: Monitoring & Management
1. Monitor deployment progress
2. Test rollback capabilities
3. Verify health checks and metrics
4. Test cost tracking and optimization

## 🛠️ Local Development

### React Frontend
```bash
cd test-apps/react-frontend
npm install
npm start
# Opens on http://localhost:3000
```

### FastAPI Backend
```bash
cd test-apps/fastapi-backend
pip install -r requirements.txt
python main.py
# Opens on http://localhost:8000
# API docs: http://localhost:8000/docs
```

## 🐳 Docker Deployment

### FastAPI Backend
```bash
cd test-apps/fastapi-backend
docker build -t codeflowops-test-api .
docker run -p 8000:8000 codeflowops-test-api
```

## 🌍 Environment Variables

### React Frontend
```env
REACT_APP_API_URL=http://localhost:8000
REACT_APP_ENVIRONMENT=development
```

### FastAPI Backend
```env
ENVIRONMENT=development
DATABASE_URL=sqlite:///./codeflowops_test.db
SECRET_KEY=your-secret-key
PORT=8000
```

## 📊 Expected Test Results

### ✅ Successful Outcomes
- **Stack Detection**: 100% accurate technology identification
- **Infrastructure**: Valid Terraform configurations generated
- **Deployment**: Applications accessible via generated URLs
- **SSL**: Automatic certificate provisioning and configuration
- **Monitoring**: Real-time deployment status and metrics

### 🔍 Validation Endpoints

#### React Frontend
- `GET /` - Application homepage
- Health check via API connection test

#### FastAPI Backend
- `GET /` - API information
- `GET /health` - Health check endpoint
- `GET /docs` - Interactive API documentation
- `GET /api/v1/status` - Detailed API status
- `POST /api/v1/auth/login` - Authentication test

## 🎯 Success Criteria

### Stack Detection (Phase 1)
- [ ] Correctly identifies React frontend
- [ ] Detects FastAPI backend
- [ ] Identifies dependencies from package.json and requirements.txt
- [ ] Recognizes build scripts and commands

### Infrastructure Generation (Phase 2)
- [ ] Generates valid AWS/GCP/Azure configurations
- [ ] Creates appropriate networking setup
- [ ] Configures load balancers and SSL
- [ ] Sets up monitoring and logging

### Deployment Success (Phase 3)
- [ ] Successful application builds
- [ ] Accessible via generated URLs
- [ ] SSL certificates working
- [ ] Environment variables properly injected
- [ ] Health checks passing

### Monitoring & Analytics (Phase 4)
- [ ] Real-time deployment status
- [ ] Performance metrics collection
- [ ] Cost tracking accuracy
- [ ] Alert system functionality

## 🔧 CodeFlowOps Integration

When connecting this repository to CodeFlowOps:

1. **Repository URL**: `https://github.com/ClayDesk/codeflowops-test-app`
2. **Expected Detection**:
   - Frontend: React 18 SPA
   - Backend: FastAPI Python application
   - Build: npm build + Docker containerization
   - Database: SQLite (upgradeable to PostgreSQL)

3. **Generated Infrastructure**:
   - S3 + CloudFront for React frontend
   - ECS Fargate for FastAPI backend
   - Application Load Balancer
   - Route 53 for custom domain
   - RDS PostgreSQL (if database scaling needed)

## 📝 Test Documentation

After running tests with CodeFlowOps, document:
- Detection accuracy
- Infrastructure quality
- Deployment success rate
- Performance metrics
- Cost analysis
- User experience feedback

## 🚀 Next Steps

1. Create GitHub repository at `https://github.com/ClayDesk/codeflowops-test-app`
2. Push test applications to separate branches
3. Configure CodeFlowOps with test cloud accounts
4. Run systematic testing scenarios
5. Document results and improvements

---

**CodeFlowOps Test Suite** - Validating AI-powered DevOps automation 🚀
