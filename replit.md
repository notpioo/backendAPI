# Academic Chatbot Backend System

## Overview
A Python Flask backend system for an academic virtual assistant chatbot with dark-themed admin panel. This system provides REST API endpoints for Flutter app integration, NLP processing using Google Gemini AI, and comprehensive knowledge base management.

## Recent Changes
- **2025-09-15**: Complete implementation of chatbot backend system
  - Flask backend with organized folder structure
  - Google Gemini 2.5 Flash integration for natural Indonesian language responses
  - Mock Firebase database for development (ready for production Firebase integration)
  - Dark-themed admin panel matching user's design specification
  - CRUD operations for knowledge base management
  - Academic-focused response filtering
  - REST API endpoints for Flutter integration

## Project Architecture
- **Backend**: Python Flask with organized MVC structure
  - `/app/routes/`: API endpoint handlers (chat, knowledge, admin)
  - `/app/services/`: Business logic (Gemini AI, Knowledge management)
  - `/app/config/`: Configuration (Firebase mock/real setup)
  - `/app/templates/`: Admin panel HTML templates
  - `/app/static/`: CSS/JS assets for dark theme

- **Database**: Mock Firebase Realtime Database (development), ready for production Firebase
- **AI Integration**: Google Gemini 2.5 Flash with academic content filtering
- **Frontend**: Dark-themed responsive admin panel with dashboard, CRUD operations, chatbot testing

## Key Features Implemented
1. **Chatbot API** (`/api/chat/message`): Natural Indonesian language responses for academic queries
2. **Knowledge Management API** (`/api/knowledge/`): CRUD operations for knowledge base
3. **Admin Panel**: Dark-themed interface with dashboard, testing, knowledge management
4. **Academic Filtering**: AI-powered filtering to ensure academic-focused responses
5. **Mobile Ready**: REST API endpoints ready for Flutter integration

## User Preferences
- Dark theme UI matching provided design
- Indonesian language for all responses
- Academic-focused content only
- Clean, organized code structure for easy maintenance
- No excessive caching for easy development updates