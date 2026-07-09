import random
from django.core.management.base import BaseCommand
from accounts.models import Account, ChatbotRole

class Command(BaseCommand):
    help = 'Seeds the database with dummy user accounts and chatbot roles'

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting database seeding...")

        # 1. Seed Chatbot Roles
        self.stdout.write("Seeding Chatbot Roles...")
        roles_data = [
            {
                "name": "Trợ lý Tiếng Anh",
                "code": "english_tutor",
                "description": "Giúp bạn sửa lỗi ngữ pháp, luyện giao tiếp và cải thiện từ vựng tiếng Anh.",
                "system_prompt": "Bạn là một giáo viên tiếng Anh bản xứ thân thiện. Hãy sửa các lỗi chính tả, ngữ pháp nếu có trong câu nói của người dùng, sau đó trả lời họ bằng tiếng Anh đơn giản, dễ hiểu."
            },
            {
                "name": "Huấn luyện viên Gym",
                "code": "gym_coach",
                "description": "Tư vấn chế độ tập luyện, lịch tập và kỹ thuật các bài tập thể hình.",
                "system_prompt": "Bạn là một huấn luyện viên thể hình chuyên nghiệp. Hãy trả lời các câu hỏi của người dùng về lịch tập, kỹ thuật tập luyện và cách xây dựng cơ bắp một cách khoa học, kỷ luật."
            },
            {
                "name": "Trợ lý Sức khỏe & Dinh dưỡng",
                "code": "health_assistant",
                "description": "Tư vấn chế độ ăn uống lành mạnh, dinh dưỡng hợp lý.",
                "system_prompt": "Bạn là chuyên gia dinh dưỡng và sức khỏe. Hãy đưa ra các lời khuyên khoa học về chế độ ăn uống, lượng calo cần thiết và thói quen sinh hoạt lành mạnh cho người dùng."
            },
            {
                "name": "Trợ lý Tiếng Trung",
                "code": "chinese_tutor",
                "description": "Giúp bạn sửa lỗi ngữ pháp, luyện giao tiếp và cải thiện từ vựng tiếng Trung.",
                "system_prompt": "Bạn là một giáo viên tiếng Trung bản xứ thân thiện. Hãy sửa các lỗi chính tả, ngữ pháp nếu có trong câu nói của người dùng, sau đó trả lời họ bằng tiếng Trung đơn giản, dễ hiểu."
            }
        ]

        roles_seeded = 0
        for r_data in roles_data:
            role, created = ChatbotRole.objects.get_or_create(
                code=r_data["code"],
                defaults={
                    "name": r_data["name"],
                    "description": r_data["description"],
                    "system_prompt": r_data["system_prompt"]
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created chatbot role: {role.name}"))
                roles_seeded += 1

        # 2. Ensure a superuser 'admin' exists
        self.stdout.write("Seeding superuser...")
        if not Account.objects.filter(username='admin').exists():
            Account.objects.create_superuser('admin', 'admin@example.com', '12345678', phone_number='0900000000')
            self.stdout.write(self.style.SUCCESS("Created superuser 'admin' with password '12345678'"))
        else:
            self.stdout.write("Superuser 'admin' already exists.")

        # 3. Create 10 dummy user accounts
        self.stdout.write("Seeding dummy users...")
        created_count = 0
        for i in range(1, 11):
            username = f'user{i}'
            email = f'{username}@gmail.com'
            password = 'password123'
            
            # Generate a mock Vietnamese phone number starting with 09, 03, 07, 08
            prefix = random.choice(['09', '03', '07', '08'])
            suffix = "".join([str(random.randint(0, 9)) for _ in range(8)])
            phone_number = prefix + suffix

            # Check if user already exists
            if not Account.objects.filter(username=username).exists():
                Account.objects.create_user(
                    username=username, 
                    email=email, 
                    password=password,
                    phone_number=phone_number
                )
                self.stdout.write(self.style.SUCCESS(f"Created user '{username}' - Email: {email} - Phone: {phone_number}"))
                created_count += 1
            else:
                self.stdout.write(f"User '{username}' already exists.")

        self.stdout.write(self.style.SUCCESS(
            f"Seeding completed! Seeded {roles_seeded} chatbot roles and {created_count} new users."
        ))
