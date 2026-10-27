from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import UserProfile
from agents.models import Agent
from customers.models import Customer

class Command(BaseCommand):
    help = "Seed demo user accounts for Seller, Customer, and Admin roles."

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING("Seeding demo accounts..."))

        # 1. Admin Account
        admin_user, _ = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@primerestates.com',
                'first_name': 'System',
                'last_name': 'Admin',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        admin_user.set_password('adminpassword123')
        admin_user.is_staff = True
        admin_user.is_superuser = True
        admin_user.save()

        admin_profile, _ = UserProfile.objects.get_or_create(user=admin_user)
        admin_profile.role = 'admin'
        admin_profile.phone = '+1 (800) 555-0199'
        admin_profile.avatar = 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=300&q=80'
        admin_profile.save()
        self.stdout.write(self.style.SUCCESS("[OK] Admin user created: admin / adminpassword123"))

        # 2. Seller / Agent Account
        agent = Agent.objects.filter(email='alex.hayes@primerestates.com').first() or Agent.objects.first()
        seller_user, _ = User.objects.get_or_create(
            username='seller_alex',
            defaults={
                'email': 'alex.hayes@primerestates.com',
                'first_name': 'Alexander',
                'last_name': 'Hayes',
            }
        )
        seller_user.set_password('password123')
        seller_user.save()

        seller_profile, _ = UserProfile.objects.get_or_create(user=seller_user)
        seller_profile.role = 'seller'
        seller_profile.phone = '+1 (305) 555-0188'
        seller_profile.company_name = 'Bespoke Realty International'
        seller_profile.agent = agent
        seller_profile.avatar = 'https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?auto=format&fit=crop&w=600&q=80'
        seller_profile.save()
        self.stdout.write(self.style.SUCCESS("[OK] Seller user created: seller_alex / password123"))

        # 3. Customer Account
        customer = Customer.objects.first()
        customer_user, _ = User.objects.get_or_create(
            username='customer_rahul',
            defaults={
                'email': 'customer.rahul@example.com',
                'first_name': 'Rahul',
                'last_name': 'Sharma',
            }
        )
        customer_user.set_password('password123')
        customer_user.save()

        customer_profile, _ = UserProfile.objects.get_or_create(user=customer_user)
        customer_profile.role = 'customer'
        customer_profile.phone = '+1 (415) 555-0921'
        customer_profile.customer = customer
        customer_profile.avatar = 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=200&q=80'
        customer_profile.save()
        self.stdout.write(self.style.SUCCESS("[OK] Customer user created: customer_rahul / password123"))
