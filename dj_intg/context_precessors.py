from django.utils import timezone
from datetime import timedelta, datetime
from .models import Progress
import random


motivational_quotes_study = [
    {"quote": "Don't forget that every effort counts and every step brings you closer to your goal. Keep persevering and you will see the results of your efforts."},
    {"quote": "Nothing is impossible for those who never back down from a challenge. Double your efforts and show the world what you're capable of."},
    {"quote": "The road to success is paved with obstacles, but with determination and hard work, you can accomplish anything. Keep pushing yourself!"},
    {"quote": "Every difficult moment is an opportunity to grow. Double your efforts and you'll be amazed at what you can achieve."},
    {"quote": "The path to success is long and sometimes difficult, but by doubling your efforts, you will achieve your dreams. Don't give up!"},
    {"quote": "Every extra effort you make today brings you a little closer to tomorrow's success. Don't give up and keep surpassing yourself."},
    

    
]
motivational_quotes_success = [
    {"quote": "Success is not the key to happiness. Happiness is the key to success. If you love what you are doing, you will be successful.", "author": "Albert Schweitzer"},
    {"quote": "The only limit to our realization of tomorrow is our doubts of today.", "author": "Franklin D. Roosevelt"},
    {"quote": "Don't be afraid to give up the good to go for the great.", "author": "John D. Rockefeller"},
    {"quote": "Success usually comes to those who are too busy to be looking for it.", "author": "Henry David Thoreau"},
    {"quote": "Opportunities don't happen. You create them.", "author": "Chris Grosser"},
    {"quote": "Success is not how high you have climbed, but how you make a positive difference to the world.", "author": "Roy T. Bennett"},
    {"quote": "I find that the harder I work, the more luck I seem to have.", "author": "Thomas Jefferson"},
    {"quote": "Success is walking from failure to failure with no loss of enthusiasm.", "author": "Winston Churchill"},
    {"quote": "The way to get started is to quit talking and begin doing.", "author": "Walt Disney"},
    {"quote": "Your time is limited, don't waste it living someone else’s life.", "author": "Steve Jobs"}
]
    





def navbar_data(request):
    if not request.user.is_authenticated:
        return {'error': 'No progress data found for the current user.'}

    user_progress = Progress.objects.filter(user=request.user)

    if not user_progress.exists():
        return {'error': 'No progress data found for the current user.'}

    response = []
    risk_levels = {'extreme': 1, 'high': 2, 'medium': 3, 'low': 4}

    for progress in user_progress:
        exam_date = progress.exam_date
        current_date = timezone.now().date()

        if exam_date <= current_date:
            continue

        exam_datetime_naive = datetime.combine(exam_date, datetime.min.time())
        exam_datetime = timezone.make_aware(exam_datetime_naive, timezone.get_current_timezone())
        remaining_time = exam_datetime - timezone.now()

        predicted_time = timedelta(days=progress.days_predicted, hours=progress.hours_predicted)

        if remaining_time < predicted_time:
            total_hours_predicted = progress.days_predicted * 24 + progress.hours_predicted
            remaining_hours = remaining_time.total_seconds() / 3600

            if remaining_hours <= total_hours_predicted * 0.25:
                risk_level = 'extreme'
            elif remaining_hours <= total_hours_predicted * 0.5:
                risk_level = 'high'
            elif remaining_hours <= total_hours_predicted * 0.75:
                risk_level = 'medium'
            else:
                risk_level = 'low'

            quote = random.choice(motivational_quotes_study + motivational_quotes_success)
            
            response.append({
                'matiere': progress.matiere,
                'risk_level': risk_level,
                'quote': quote
            })

    if not response:
        return {'message': 'No exams found within the risk calculation criteria.'}

    response.sort(key=lambda x: risk_levels.get(x['risk_level'], 999))

    return {'navbar_data': response}