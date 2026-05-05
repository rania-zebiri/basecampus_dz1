# 🎓 BaseCampus Dz — Smart Campus Companion

A production-style mobile application built with **Flutter & Dart** for university campus daily life management. The app demonstrates essential **Mobile OS concepts** including offline-first architecture, device feature integration, local notifications, secure storage, and background execution.

---

## 📱 Features

### Student Side
- 🔐 **Authentication** — Email/password login & registration with JWT tokens
- 🏠 **Home Dashboard** — Today's schedule + latest announcements
- 📅 **Timetable** — Full weekly schedule with current class indicator
- 📣 **Announcements** — Real-time announcements with category filtering
- 📆 **Events** — Campus events with weekly calendar navigation
- 🗺️ **Campus Map** — Interactive OpenStreetMap with Points of Interest
- 🔔 **Notifications** — Push notifications with read/unread status
- ⚙️ **Settings** — Dark mode, language, class reminders, export schedule
- 📴 **Offline Mode** — Browse cached content without internet connection

---

## 📐 Mobile OS Concepts Demonstrated

| Feature | OS Concept |
|---------|-----------|
| JWT + FlutterSecureStorage | Security & Sandboxing |
| REST API + Dio | Networking |
| SharedPreferences | Local Storage |
| flutter_local_notifications | Background Execution & Notifications |
| Connectivity detection | Networking Awareness |
| App lifecycle handlers | App Lifecycle |
| Offline banner + cached data | Offline-First Architecture |

---

## 🏗️ Architecture

The project follows **Clean Architecture** principles:

```
lib/
  core/
    constants/        ← API endpoints
    network/          ← Dio client setup
    services/         ← Notification service
  data/
    models/           ← Data models (User, Announcement, Event, Timetable...)
    sources/          ← Remote & Local data sources
  domain/
    repositories/     ← Business logic layer
  presentation/
    screens/          ← UI screens
    widgets/          ← Reusable widgets
```

---

## 🛠️ Tech Stack

### Frontend (Flutter)

| Package | Purpose |
|---------|---------|
| `dio` | HTTP client |
| `flutter_secure_storage` | Secure token storage |
| `shared_preferences` | Local settings storage |
| `flutter_local_notifications` | Local push notifications |
| `flutter_map` + `latlong2` | Interactive campus map |
| `connectivity_plus` | Network state detection |
| `local_auth` | Biometric authentication |
| `image_picker` | Camera/gallery access |
| `permission_handler` | Runtime permissions |
| `geolocator` | GPS location |

### Backend (FastAPI + Supabase)

| Technology | Purpose |
|-----------|---------|
| `FastAPI` | REST API framework |
| `Supabase` | PostgreSQL database |
| `JWT (python-jose)` | Token authentication |
| `bcrypt` | Password hashing |
| `uvicorn` | ASGI server |

---

## 🗄️ Database Schema

```sql
users          → Authentication & profile
announcements  → Campus announcements (Academic/Events/Safety)
events         → Campus events with date/time
timetable      → Weekly class schedule
notifications  → Push notification records
```

---

## 🚀 Getting Started

### Prerequisites
- Flutter SDK (stable)
- Python 3.12+
- Supabase account

### Backend Setup

```bash
cd basecampus-backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create `.env` file in `basecampus-backend/`:

```env
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_anon_key
SUPABASE_SERVICE_KEY=your_service_role_key
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080
```

Run the server:

```bash
uvicorn app.main:app --reload
```

### Flutter Setup

```bash
cd basecampus_dz
flutter pub get
flutter run
```

---

## 📡 API Endpoints

### Authentication
```
POST   /auth/register         → Register new student
POST   /auth/login            → Login & get JWT token
GET    /auth/me               → Get current user
```

### Announcements
```
GET    /announcements/        → Get all announcements
GET    /announcements/{id}    → Get single announcement
POST   /announcements/        → Create announcement
PUT    /announcements/{id}    → Update announcement
DELETE /announcements/{id}    → Delete announcement
```

### Events
```
GET    /events/               → Get events (filter by date)
GET    /events/{id}           → Get single event
POST   /events/               → Create event
PUT    /events/{id}           → Update event
DELETE /events/{id}           → Delete event
```

### Timetable
```
GET    /timetable/            → Get timetable (filter by day)
GET    /timetable/today       → Get today's classes
```

### Notifications
```
GET    /notifications/              → Get all notifications
PUT    /notifications/{id}/read     → Mark as read
PUT    /notifications/read-all      → Mark all as read
```

---

## 📁 Project Structure

```
Full app/
├── basecampus_dz/          ← Flutter mobile app
│   ├── lib/
│   │   ├── core/
│   │   │   ├── constants/
│   │   │   ├── network/
│   │   │   └── services/
│   │   ├── data/
│   │   │   ├── models/
│   │   │   └── sources/
│   │   ├── domain/
│   │   │   └── repositories/
│   │   └── presentation/
│   │       ├── screens/
│   │       └── widgets/
│   └── pubspec.yaml
└── basecampus-backend/     ← FastAPI backend
    ├── app/
    │   ├── api/
    │   │   └── routes/
    │   ├── core/
    │   └── schemas/
    ├── requirements.txt
    └── main.py
```

---

## 🗺️ App Screens

| Screen | Description |
|--------|-------------|
| Splash | App loading with logo |
| Onboarding | 3-step introduction |
| Login | Email/password authentication |
| Register | 3-step student registration |
| Home | Dashboard with schedule & announcements |
| Timetable | Weekly class schedule |
| Announcements | Campus announcements with filters |
| Events | Campus events by date |
| Map | Interactive campus map |
| Notifications | Push notifications center |
| Settings | App preferences & profile |
| Forgot Password | 3-step password reset |

---
