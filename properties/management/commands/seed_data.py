import random
from datetime import date, timedelta
from django.core.management.base import BaseCommand
from agents.models import Agent
from customers.models import Customer
from properties.models import Property, PropertyImage
from appointments.models import Appointment
from reviews.models import Review

class Command(BaseCommand):
    help = "Seeds database with high-end realistic real estate listings, agents, appointments, and reviews."

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING("Starting database seed..."))

        # Clear existing data
        Review.objects.all().delete()
        Appointment.objects.all().delete()
        PropertyImage.objects.all().delete()
        Property.objects.all().delete()
        Customer.objects.all().delete()
        Agent.objects.all().delete()

        # 1. Create Agents
        agents_data = [
            {
                "name": "Eleanor Vance",
                "email": "eleanor.vance@primerestates.com",
                "phone": "+1 (310) 555-0142",
                "bio": "Specializing in premier luxury estates and architectural landmarks across Southern California with over 12 years of industry leadership.",
                "avatar": "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?auto=format&fit=crop&w=600&q=80",
                "experience_years": 12,
                "rating": 4.95,
                "rating_count": 48,
                "agency_name": "Prime Luxury Estates",
            },
            {
                "name": "Marcus Sterling",
                "email": "marcus.sterling@primerestates.com",
                "phone": "+1 (212) 555-0198",
                "bio": "Managing Partner with deep expertise in waterfront penthouses, trophy assets, and investment portfolios.",
                "avatar": "https://images.unsplash.com/photo-1560250097-0b93528c311a?auto=format&fit=crop&w=600&q=80",
                "experience_years": 15,
                "rating": 4.98,
                "rating_count": 62,
                "agency_name": "Sterling & Co. Real Estate",
            },
            {
                "name": "Sophia Chen",
                "email": "sophia.chen@primerestates.com",
                "phone": "+1 (415) 555-0177",
                "bio": "Specialized in high-tech sustainable villas, contemporary urban lofts, and international relocation clients.",
                "avatar": "https://images.unsplash.com/photo-1580489944761-15a19d654956?auto=format&fit=crop&w=600&q=80",
                "experience_years": 8,
                "rating": 4.88,
                "rating_count": 34,
                "agency_name": "Prime Luxury Estates",
            },
            {
                "name": "Alexander Hayes",
                "email": "alex.hayes@primerestates.com",
                "phone": "+1 (305) 555-0188",
                "bio": "Recognized top producer in coastal estates, luxury developments, and bespoke architectural residences.",
                "avatar": "https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?auto=format&fit=crop&w=600&q=80",
                "experience_years": 10,
                "rating": 4.91,
                "rating_count": 41,
                "agency_name": "Bespoke Realty International",
            }
        ]

        created_agents = []
        for a_data in agents_data:
            agent = Agent.objects.create(**a_data)
            created_agents.append(agent)
            self.stdout.write(f"Created Agent: {agent.name}")

        # 2. Create Customers
        customers_data = [
            {
                "name": "David Miller",
                "email": "david.miller@techcorp.io",
                "phone": "+1 (415) 890-1234",
                "avatar": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=400&q=80",
                "preferred_location": "Beverly Hills, CA",
                "budget_max": 5500000.00,
                "customer_type": "buyer",
                "status": "active",
                "notes": "Looking for 4+ bed modern villa with pool and private security.",
            },
            {
                "name": "Sarah Jenkins",
                "email": "sarah.jenkins@capitalgroup.com",
                "phone": "+1 (212) 745-9821",
                "avatar": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=400&q=80",
                "preferred_location": "Miami Beach, FL",
                "budget_max": 3500000.00,
                "customer_type": "investor",
                "status": "active",
                "notes": "Interested in turnkey oceanfront penthouses for short-term and corporate leases.",
            },
            {
                "name": "Robert & Chloe Vance",
                "email": "robert.vance@archstudio.design",
                "phone": "+1 (303) 621-4432",
                "avatar": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?auto=format&fit=crop&w=400&q=80",
                "preferred_location": "Aspen, CO",
                "budget_max": 4000000.00,
                "customer_type": "buyer",
                "status": "active",
                "notes": "Architect couple seeking contemporary mountain residence with scenic vistas.",
            },
            {
                "name": "Marcus Aurelius Vance",
                "email": "marcus.aurelius@luxholdings.com",
                "phone": "+1 (310) 902-3341",
                "avatar": "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?auto=format&fit=crop&w=400&q=80",
                "preferred_location": "Palo Alto, CA",
                "budget_max": 6000000.00,
                "customer_type": "buyer",
                "status": "active",
                "notes": "Tech entrepreneur seeking smart home with EV charging and guest house.",
            },
            {
                "name": "Elena Rostova",
                "email": "elena.rostova@globalventures.ch",
                "phone": "+1 (646) 321-7788",
                "avatar": "https://images.unsplash.com/photo-1544005313-94ddf0286df2?auto=format&fit=crop&w=400&q=80",
                "preferred_location": "New York, NY",
                "budget_max": 2000000.00,
                "customer_type": "renter",
                "status": "lead",
                "notes": "Looking for luxury furnished Tribeca or Soho loft for 2-year lease.",
            },
        ]

        created_customers = []
        for c_data in customers_data:
            customer = Customer.objects.create(**c_data)
            created_customers.append(customer)
            self.stdout.write(f"Created Customer: {customer.name}")

        # 3. Create Properties
        properties_data = [
            {
                "title": "The Glass Pavilion & Botanical Estate",
                "description": "An architectural masterpiece set behind private gates in Beverly Hills. Features 14-foot floor-to-ceiling motorized Fleetwood glass walls, infinity-edge heated pool, temperature-controlled 800-bottle wine gallery, wellness spa, and lush manicured private grounds.",
                "price": 4850000.00,
                "property_type": "villa",
                "status": "available",
                "purpose": "buy",
                "bedrooms": 5,
                "bathrooms": 6,
                "area_sqft": 6450,
                "location": "Beverly Hills, CA",
                "address": "1048 Shadow Hill Way, Beverly Hills, CA 90210",
                "latitude": 34.084120,
                "longitude": -118.409940,
                "featured": True,
                "year_built": 2023,
                "main_image": "https://images.unsplash.com/photo-1613490493576-7fde63acd811?auto=format&fit=crop&w=1200&q=80",
                "amenities": ["Infinity Pool", "Wine Cellar", "Smart Home Automation", "Spa & Sauna", "Home Cinema", "Sub-Zero Chef Kitchen", "3-Car Garage", "Security System"],
                "agent": created_agents[0],
                "gallery": [
                    "https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?auto=format&fit=crop&w=1000&q=80",
                    "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=1000&q=80",
                    "https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?auto=format&fit=crop&w=1000&q=80",
                    "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=1000&q=80",
                ]
            },
            {
                "title": "Azure Coastal Penthouse Sky Villa",
                "description": "Perched on the 38th floor in premier South Beach, this duplex penthouse commands 360-degree panoramic ocean and skyline views. Features private rooftop terrace with plunge pool, Italian custom marble kitchen, and private elevator landing.",
                "price": 2950000.00,
                "property_type": "penthouse",
                "status": "available",
                "purpose": "buy",
                "bedrooms": 3,
                "bathrooms": 4,
                "area_sqft": 3420,
                "location": "Miami Beach, FL",
                "address": "2201 Collins Avenue, PH-38, Miami Beach, FL 33139",
                "latitude": 25.798110,
                "longitude": -80.127880,
                "featured": True,
                "year_built": 2022,
                "main_image": "https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?auto=format&fit=crop&w=1200&q=80",
                "amenities": ["Private Rooftop Pool", "Oceanfront Views", "Private Elevator", "Valet Concierge", "Fitness Center", "Wraparound Balcony"],
                "agent": created_agents[3],
                "gallery": [
                    "https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?auto=format&fit=crop&w=1000&q=80",
                    "https://images.unsplash.com/photo-1560185007-cde436f6a4d0?auto=format&fit=crop&w=1000&q=80",
                    "https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?auto=format&fit=crop&w=1000&q=80",
                ]
            },
            {
                "title": "Modern Alpine Lodge & Mountain Sanctuary",
                "description": "Nestled in Red Mountain Aspen, this modern architectural sanctuary pairs rugged cedar and quartzite with contemporary glass. Features ski-in/ski-out convenience, heated stone motor court, dual master wings, and soaring cathedral ceilings.",
                "price": 3400000.00,
                "property_type": "house",
                "status": "available",
                "purpose": "buy",
                "bedrooms": 4,
                "bathrooms": 5,
                "area_sqft": 4200,
                "location": "Aspen, CO",
                "address": "450 Red Mountain Road, Aspen, CO 81611",
                "latitude": 39.198320,
                "longitude": -106.824210,
                "featured": False,
                "year_built": 2021,
                "main_image": "https://images.unsplash.com/photo-1518780664697-55e3ad937233?auto=format&fit=crop&w=1200&q=80",
                "amenities": ["Ski-in/Ski-out", "Heated Motor Court", "Stone Fireplace", "Hot Tub", "Wine Room", "Mountain Panoramic Views"],
                "agent": created_agents[1],
                "gallery": [
                    "https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?auto=format&fit=crop&w=1000&q=80",
                    "https://images.unsplash.com/photo-1584622650111-993a426fbf0a?auto=format&fit=crop&w=1000&q=80",
                ]
            },
            {
                "title": "Tribeca Historic Cast-Iron Loft",
                "description": "Authentic full-floor loft with original Corinthian cast-iron columns, exposed timber beams, 13-foot ceilings, and direct key-locked elevator access. Renovated with Poliform cabinetry and Miele appliances.",
                "price": 8500.00,
                "property_type": "apartment",
                "status": "available",
                "purpose": "rent",
                "bedrooms": 2,
                "bathrooms": 2,
                "area_sqft": 2100,
                "location": "New York, NY",
                "address": "74 Franklin Street, 4th Floor, New York, NY 10013",
                "latitude": 40.718320,
                "longitude": -74.004920,
                "featured": True,
                "year_built": 2020,
                "main_image": "https://images.unsplash.com/photo-1502005229762-ee1b2b8ab98f?auto=format&fit=crop&w=1200&q=80",
                "amenities": ["Keyed Elevator", "Cast-Iron Columns", "Exposed Brick", "Chef's Kitchen", "Storage Unit", "Pet Friendly"],
                "agent": created_agents[1],
                "gallery": [
                    "https://images.unsplash.com/photo-1505691938895-1758d7feb511?auto=format&fit=crop&w=1000&q=80",
                    "https://images.unsplash.com/photo-1560448204-61dc36dc98c8?auto=format&fit=crop&w=1000&q=80",
                ]
            },
            {
                "title": "Silicon Valley Net-Zero Smart Villa",
                "description": "A paradigm of modern sustainable luxury in prestigious Old Palo Alto. Fully integrated Tesla solar roof, Powerwall energy storage, floor-to-ceiling glass corridors, zero-edge saline pool, and detached private guest cabana.",
                "price": 5200000.00,
                "property_type": "villa",
                "status": "available",
                "purpose": "buy",
                "bedrooms": 5,
                "bathrooms": 5,
                "area_sqft": 5800,
                "location": "Palo Alto, CA",
                "address": "1420 University Avenue, Palo Alto, CA 94301",
                "latitude": 37.447380,
                "longitude": -122.148390,
                "featured": True,
                "year_built": 2024,
                "main_image": "https://images.unsplash.com/photo-1600585154526-990dced4db0d?auto=format&fit=crop&w=1200&q=80",
                "amenities": ["Solar & Powerwall", "Saline Pool", "Guest House", "EV Fast Charging", "Lutron Lighting", "Smart Irrigation"],
                "agent": created_agents[2],
                "gallery": [
                    "https://images.unsplash.com/photo-1600566753376-12c8ab7fb75b?auto=format&fit=crop&w=1000&q=80",
                    "https://images.unsplash.com/photo-1600573472592-401b489a3cdc?auto=format&fit=crop&w=1000&q=80",
                ]
            },
            {
                "title": "The Luminary High-Rise Penthouse",
                "description": "Downtown Austin high-rise residence offering uninterrupted views of Lady Bird Lake and the Texas Capitol. Amenities include 24/7 concierge, infinity pool on the 30th floor, club room, and private garage parking.",
                "price": 950000.00,
                "property_type": "apartment",
                "status": "available",
                "purpose": "buy",
                "bedrooms": 2,
                "bathrooms": 2,
                "area_sqft": 1420,
                "location": "Austin, TX",
                "address": "300 Colorado Street, Austin, TX 78701",
                "latitude": 30.266280,
                "longitude": -97.745420,
                "featured": False,
                "year_built": 2022,
                "main_image": "https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?auto=format&fit=crop&w=1200&q=80",
                "amenities": ["24/7 Concierge", "Rooftop Pool", "Lake Views", "Fitness Club", "EV Parking", "Dog Park"],
                "agent": created_agents[3],
                "gallery": [
                    "https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?auto=format&fit=crop&w=1000&q=80",
                ]
            },
            {
                "title": "Bel Air Mediterranean Heritage Estate",
                "description": "Historic grand compound featuring championship tennis court, Olympic lap pool, detached two-bedroom guest cottage, 12-seat screening theater, and expansive rolling lawns with mature olive groves.",
                "price": 7500000.00,
                "property_type": "villa",
                "status": "sold",
                "purpose": "buy",
                "bedrooms": 6,
                "bathrooms": 7,
                "area_sqft": 8500,
                "location": "Los Angeles, CA",
                "address": "10830 Bellagio Road, Los Angeles, CA 90077",
                "latitude": 34.079200,
                "longitude": -118.448500,
                "featured": False,
                "year_built": 2019,
                "main_image": "https://images.unsplash.com/photo-1580587771525-78b9dba3b914?auto=format&fit=crop&w=1200&q=80",
                "amenities": ["Tennis Court", "Theater Room", "Olympic Pool", "Guest House", "Olive Groves", "Gated Security"],
                "agent": created_agents[0],
                "gallery": [
                    "https://images.unsplash.com/photo-1600607687920-4e2a09cf159d?auto=format&fit=crop&w=1000&q=80",
                ]
            },
            {
                "title": "Sunset Plaza Designer Terrace Loft",
                "description": "High above Sunset Strip with sweeping city-to-ocean vistas. Features open-concept gallery living, private cedar terrace, smart kitchen, and private enclosed garage.",
                "price": 4200.00,
                "property_type": "apartment",
                "status": "rented",
                "purpose": "rent",
                "bedrooms": 1,
                "bathrooms": 2,
                "area_sqft": 1150,
                "location": "West Hollywood, CA",
                "address": "1280 Sunset Plaza Drive, West Hollywood, CA 90069",
                "latitude": 34.093120,
                "longitude": -118.379240,
                "featured": False,
                "year_built": 2021,
                "main_image": "https://images.unsplash.com/photo-1522771739844-6a9f6d5f14af?auto=format&fit=crop&w=1200&q=80",
                "amenities": ["City Skyline View", "Designer Terrace", "Hardwood Floors", "In-Unit Laundry", "Covered Parking"],
                "agent": created_agents[0],
                "gallery": [
                    "https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?auto=format&fit=crop&w=1000&q=80",
                ]
            },
        ]

        created_properties = []
        for p_data in properties_data:
            gallery = p_data.pop('gallery', [])
            prop = Property.objects.create(**p_data)
            for idx, img_url in enumerate(gallery):
                PropertyImage.objects.create(property=prop, image_url=img_url, order=idx+1)
            created_properties.append(prop)
            self.stdout.write(f"Created Property: {prop.title}")

        # 4. Create Appointments
        today = date.today()
        appointments_data = [
            {
                "property": created_properties[0],
                "customer": created_customers[0],
                "agent": created_properties[0].agent,
                "customer_name": created_customers[0].name,
                "customer_email": created_customers[0].email,
                "customer_phone": created_customers[0].phone,
                "appointment_date": today + timedelta(days=2),
                "time_slot": "10:00 AM - 11:00 AM",
                "status": "confirmed",
                "notes": "Client requested private walkthrough with their architect.",
            },
            {
                "property": created_properties[1],
                "customer": created_customers[1],
                "agent": created_properties[1].agent,
                "customer_name": created_customers[1].name,
                "customer_email": created_customers[1].email,
                "customer_phone": created_customers[1].phone,
                "appointment_date": today + timedelta(days=3),
                "time_slot": "02:00 PM - 03:00 PM",
                "status": "pending",
                "notes": "Interested in HOA fees and rental yield documents.",
            },
            {
                "property": created_properties[4],
                "customer": created_customers[3],
                "agent": created_properties[4].agent,
                "customer_name": created_customers[3].name,
                "customer_email": created_customers[3].email,
                "customer_phone": created_customers[3].phone,
                "appointment_date": today + timedelta(days=5),
                "time_slot": "11:30 AM - 12:30 PM",
                "status": "pending",
                "notes": "Inquiring about solar battery warranty and home security integration.",
            },
            {
                "property": created_properties[2],
                "customer": created_customers[2],
                "agent": created_properties[2].agent,
                "customer_name": created_customers[2].name,
                "customer_email": created_customers[2].email,
                "customer_phone": created_customers[2].phone,
                "appointment_date": today - timedelta(days=4),
                "time_slot": "04:00 PM - 05:00 PM",
                "status": "completed",
                "notes": "Showed Aspen mountain lodge; client loved the cathedral ceilings.",
            },
        ]

        for appt_data in appointments_data:
            appt = Appointment.objects.create(**appt_data)
            self.stdout.write(f"Created Appointment for {appt.customer_name}")

        # 5. Create Reviews
        reviews_data = [
            {
                "property": created_properties[0],
                "author_name": "Julian Sterling, AIA",
                "rating": 5,
                "comment": "The architectural scale and craftsmanship of this estate are extraordinary. The Fleetwood glass walls seamlessly blur interior and garden.",
            },
            {
                "property": created_properties[0],
                "author_name": "Catherine Dupont",
                "rating": 5,
                "comment": "Unbelievable sunset views from the infinity pool. The temperature-controlled wine room is a connoisseur's dream.",
            },
            {
                "property": created_properties[1],
                "author_name": "Anthony Moretti",
                "rating": 5,
                "comment": "The finest penthouse in South Beach. Private rooftop pool provides unmatched privacy while looking over the Atlantic.",
            },
            {
                "property": created_properties[2],
                "author_name": "Klaus Lindner",
                "rating": 5,
                "comment": "Flawless ski-in/ski-out experience. The radiant heating throughout the driveway and motor court worked effortlessly.",
            },
            {
                "property": created_properties[3],
                "author_name": "Maya Lin",
                "rating": 4,
                "comment": "Incredible natural light and preserved historic cast-iron details. Prime location right off Franklin Street.",
            },
            {
                "property": created_properties[4],
                "author_name": "Vikram Patel",
                "rating": 5,
                "comment": "The pinnacle of energy-independent smart living in Palo Alto. Truly rare construction quality.",
            },
        ]

        for rev_data in reviews_data:
            Review.objects.create(**rev_data)

        self.stdout.write(self.style.SUCCESS("Database successfully seeded with luxury real estate data!"))
