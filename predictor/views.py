from django.shortcuts import render
from django.contrib import messages

def index(request):
    """
    Single view that handles both home and predictor
    """
    context = {
        'show_predictor': False,
        'prediction': None
    }
    
    if request.method == 'POST':
        # User submitted the form - show predictor section
        context['show_predictor'] = True
        
        try:
            # Get form data
            age = request.POST.get('age')
            gender = request.POST.get('gender')
            heart_rate_bpm = request.POST.get('heart_rate_bpm')
            systolic_bp = request.POST.get('systolic_bp')
            diastolic_bp = request.POST.get('diastolic_bp')
            temperature_c = request.POST.get('temperature_c')
            spo2_percent = request.POST.get('spo2_percent')
            bmi = request.POST.get('bmi')
            has_diabetes = request.POST.get('has_diabetes')
            smoker = request.POST.get('smoker')
            
            # Validate all fields are present
            if not all([age, gender, heart_rate_bpm, systolic_bp, diastolic_bp, 
                       temperature_c, spo2_percent, bmi, has_diabetes, smoker]):
                messages.error(request, 'All fields are required.')
                # Keep form values
                context.update(request.POST.dict())
                return render(request, 'index.html', context)
            
            # Convert to appropriate types
            try:
                age = int(age)
                gender = int(gender)
                heart_rate_bpm = int(heart_rate_bpm)
                systolic_bp = int(systolic_bp)
                diastolic_bp = int(diastolic_bp)
                temperature_c = float(temperature_c)
                spo2_percent = int(spo2_percent)
                bmi = float(bmi)
                has_diabetes = int(has_diabetes)
                smoker = int(smoker)
            except ValueError:
                messages.error(request, 'Invalid input values. Please check your entries.')
                context.update(request.POST.dict())
                return render(request, 'index.html', context)
            
            # Validate ranges
            errors = []
            if not (0 <= age <= 120):
                errors.append('Age must be between 0 and 120')
            if not (40 <= heart_rate_bpm <= 200):
                errors.append('Heart rate must be between 40 and 200')
            if not (70 <= systolic_bp <= 250):
                errors.append('Systolic BP must be between 70 and 250')
            if not (40 <= diastolic_bp <= 150):
                errors.append('Diastolic BP must be between 40 and 150')
            if not (35 <= temperature_c <= 42):
                errors.append('Temperature must be between 35 and 42')
            if not (70 <= spo2_percent <= 100):
                errors.append('SpO2 must be between 70 and 100')
            if not (10 <= bmi <= 60):
                errors.append('BMI must be between 10 and 60')
            
            if errors:
                for error in errors:
                    messages.error(request, error)
                context.update(request.POST.dict())
                return render(request, 'index.html', context)
            
            # Prepare data for prediction
            patient_data = {
                'age': age,
                'gender': gender,
                'heart_rate_bpm': heart_rate_bpm,
                'systolic_bp': systolic_bp,
                'diastolic_bp': diastolic_bp,
                'temperature_c': temperature_c,
                'spo2_percent': spo2_percent,
                'bmi': bmi,
                'has_diabetes': has_diabetes,
                'smoker': smoker
            }
            
            # Calculate prediction (replace with your ML model)
            prediction = calculate_demo_risk(patient_data)
            
            context['prediction'] = prediction
            context.update(request.POST.dict())
            messages.success(request, 'Risk assessment completed successfully!')
            
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')
            context.update(request.POST.dict())
    
    return render(request, 'predictor/form.html', context)



def calculate_demo_risk(data):
    """
    Demo risk calculation - replace with your ML model
    """
    risk_score = 0
    
    # Age factor
    if data['age'] > 60:
        risk_score += 2
    elif data['age'] > 45:
        risk_score += 1
    
    # Blood pressure
    if data['systolic_bp'] > 140 or data['diastolic_bp'] > 90:
        risk_score += 2
    
    # Heart rate
    if data['heart_rate_bpm'] > 100 or data['heart_rate_bpm'] < 60:
        risk_score += 1
    
    # SpO2
    if data['spo2_percent'] < 95:
        risk_score += 2
    
    # BMI
    if data['bmi'] > 30 or data['bmi'] < 18.5:
        risk_score += 1
    
    # Diabetes
    if data['has_diabetes'] == 1:
        risk_score += 2
    
    # Smoking
    if data['smoker'] == 1:
        risk_score += 2
    
    # Temperature
    if data['temperature_c'] > 38.0:
        risk_score += 1
    
    # Determine risk level
    if risk_score >= 7:
        return "High Risk"
    elif risk_score >= 4:
        return "Medium Risk"
    else:
        return "Low Risk"