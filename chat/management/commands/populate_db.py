# chat/management/commands/populate_admission_data.py
from django.core.management.base import BaseCommand
from chat.models import FAQ, AdmissionInfo

class Command(BaseCommand):
    help = 'Populate admission data'

    def handle(self, *args, **options):
        # Clear existing data
        FAQ.objects.all().delete()
        AdmissionInfo.objects.all().delete()

        # Add FAQs
        faqs = [
            {
                'question': 'What documents do I need to submit for admission to Akanu Ibiam Federal Polytechnic Unwana?',
                'answer': 'You must submit: Completed application form, Official high school transcripts, Standardized test scores (WAEC/NECO/NABTEB), Two letters of recommendation, Personal statement essay, Application fee (₦20,000)',
                'category': 'requirements'
            },
            {
                'question': 'What programs does Akanu Ibiam Federal Polytechnic Unwana offer?',
                'answer': 'We offer National Diploma (ND) and Higher National Diploma (HND) programs in: Engineering Technology, Applied Sciences, Business Studies, Environmental Studies, Information Technology, General Studies',
                'category': 'programs'
            },
            {
                'question': 'What is the application deadline for Akanu Ibiam Federal Polytechnic Unwana?',
                'answer': 'ND Full-Time: June 30, ND Part-Time: August 15, HND Full-Time: July 31, HND Part-Time: September 15',
                'category': 'deadlines'
            },
            {
                'question': 'How do I apply for financial aid at Akanu Ibiam Federal Polytechnic Unwana?',
                'answer': 'Complete the polytechnic\'s financial aid application, Submit JAMB result slip, Provide family income documentation, Demonstrate academic merit',
                'category': 'financial_aid'
            },
            {
                'question': 'Can I transfer credits from another polytechnic to Akanu Ibiam Federal Polytechnic Unwana?',
                'answer': 'Yes, if: Courses were completed at an accredited polytechnic, Grade earned was Credit or better, Course content aligns with our curriculum, Credits are less than 5 years old',
                'category': 'transfers'
            }
        ]

        for faq in faqs:
            FAQ.objects.create(
                question=faq['question'],
                answer=faq['answer'],
                category=faq['category']
            )

        # Add general information
        AdmissionInfo.objects.create(
            title="About Akanu Ibiam Federal Polytechnic Unwana",
            content="Akanu Ibiam Federal Polytechnic Unwana is a leading polytechnic in Nigeria offering quality technical education.",
            category="about"
        )

        self.stdout.write(self.style.SUCCESS('Successfully populated admission data'))