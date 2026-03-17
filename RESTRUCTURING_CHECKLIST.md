# 📋 Directory Restructuring Guide

## ✅ Completed Automatically

- ✅ Created `src/backend/models/` folder
- ✅ Created `src/backend/routes/` folder  
- ✅ Created `training/data/` folder
- ✅ Created `training/tests/` folder
- ✅ Created `config.py` with correct paths
- ✅ Created `routes/heart.py` with correct paths
- ✅ Created `routes/lung.py` with correct paths
- ✅ Updated `test_lung.py` with relative paths
- ✅ Updated `test_model.py` with relative paths
- ✅ Updated `test_real.py` with relative paths
- ✅ Updated `app.py` with new structure

---

## 🚚 Manual Steps Required

### **Step 1: Move Model Files**

Run these commands in PowerShell from `src\backend\`:

```powershell
cd C:\Users\ANIxP\Documents\MultiDiseasePrediction\src\backend

# Move heart model
Move-Item heart.pkl models\heart.pkl

# Move lung model
Move-Item lung_cancer_detection_model.keras models\lung_cancer_detection_model.keras
```

**Verify:** You should now have:
- `src/backend/models/heart.pkl` ✅
- `src/backend/models/lung_cancer_detection_model.keras` ✅

---

### **Step 2: Move Test Files**

Run from `src\backend\`:

```powershell
# Move test files
Move-Item test_lung.py ..\..\training\tests\test_lung.py
Move-Item test_model.py ..\..\training\tests\test_model.py
Move-Item test_real.py ..\..\training\tests\test_real.py
Move-Item test_image.jpeg ..\..\training\tests\test_image.jpeg
```

**Verify:** You should now have:
- `training/tests/test_lung.py` ✅
- `training/tests/test_model.py` ✅
- `training/tests/test_real.py` ✅
- `training/tests/test_image.jpeg` ✅

---

### **Step 3: Delete Old/Empty Files (Optional)**

Delete these files from `src/backend/` if they still exist:
- `heart.pkl` (moved to models/)
- `lung_cancer_detection_model.keras` (moved to models/)
- `test_lung.py` (moved to training/tests/)
- `test_model.py` (moved to training/tests/)
- `test_real.py` (moved to training/tests/)
- `test_image.jpeg` (moved to training/tests/)

---

## 🗂️ Final Directory Structure

After completing the above steps, your project should look like:

```
MultiDiseasePrediction/
├── src/
│   ├── backend/
│   │   ├── app.py                    ✅
│   │   ├── config.py                 ✅
│   │   ├── 📁 models/
│   │   │   ├── heart.pkl             👈 MOVE HERE
│   │   │   └── lung_cancer_detection_model.keras  👈 MOVE HERE
│   │   ├── 📁 routes/
│   │   │   ├── __init__.py           ✅
│   │   │   ├── heart.py              ✅
│   │   │   └── lung.py               ✅
│   │   └── 📁 uploads/               (auto-created)
│   │
│   └── frontend/                      ✅
│
├── training/
│   ├── *.ipynb                        ✅
│   ├── 📁 data/
│   │   ├── heart.csv                 (download from Kaggle)
│   │   └── lung_images/              (download from Kaggle)
│   │
│   └── 📁 tests/
│       ├── test_lung.py              👈 MOVE HERE
│       ├── test_model.py             👈 MOVE HERE
│       ├── test_real.py              👈 MOVE HERE
│       └── test_image.jpeg           👈 MOVE HERE
│
└── MDvenv/                            ✅
```

---

## 🔧 Testing After Restructuring

### Test heart model:
```powershell
cd training\tests
python test_model.py
```

### Test lung model (dummy):
```powershell
python test_lung.py
```

### Test lung model (real image):
```powershell
python test_real.py
```

---

## ✨ Code Updates Summary

All Python files have been updated to use **relative paths** so they work from anywhere:

- `heart.py` - loads from `models/heart.pkl` ✅
- `lung.py` - loads from `models/lung_cancer_detection_model.keras` ✅
- `app.py` - imports from `routes` ✅
- Test files - use relative paths with `os.path` ✅

---

## 🚀 Next: Start the Application

Once restructuring is complete:

```powershell
# Terminal 1 - Backend
cd src\backend
python app.py

# Terminal 2 - Frontend  
cd src\frontend
npm start
```

✅ Your app is now properly organized and ready to go!
