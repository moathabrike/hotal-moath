#!/usr/bin/env python3
"""
إنشاء بيانات تجريبية لنظام إدارة فندق لؤلؤة درنة
Create Sample Data for Luluat Derna Hotel Management System
"""

import os
import sys
from datetime import date, datetime, timedelta
import random

# إضافة مسار التطبيق
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import User, Room, RoomType, Booking, Payment

def create_sample_data():
    """إنشاء بيانات تجريبية"""
    
    app = create_app('development')
    
    with app.app_context():
        print("إنشاء البيانات التجريبية...")
        
        # إنشاء قاعدة البيانات
        db.create_all()
        
        # إنشاء أنواع الغرف إذا لم تكن موجودة
        if not RoomType.query.first():
            print("إضافة أنواع الغرف...")
            
            room_types_data = [
                {
                    'name': 'غرفة عادية',
                    'description': 'غرفة مريحة مع جميع المرافق الأساسية للإقامة المثالية',
                    'base_price': 200.0,
                    'capacity': 2,
                    'amenities': 'تكييف، تلفزيون LED 32 بوصة، واي فاي مجاني، حمام خاص، ثلاجة صغيرة، خزنة، مجفف شعر'
                },
                {
                    'name': 'غرفة ديلوكس',
                    'description': 'غرفة فاخرة مع إطلالة رائعة ومرافق متقدمة لتجربة استثنائية',
                    'base_price': 350.0,
                    'capacity': 2,
                    'amenities': 'تكييف، تلفزيون ذكي 43 بوصة، واي فاي مجاني، حمام فاخر مع بانيو، ميني بار، شرفة، خدمة الغرف'
                },
                {
                    'name': 'جناح عائلي',
                    'description': 'جناح واسع مناسب للعائلات مع غرفة معيشة منفصلة ومرافق شاملة',
                    'base_price': 500.0,
                    'capacity': 4,
                    'amenities': 'تكييف، تلفزيون ذكي 55 بوصة، واي فاي مجاني، حمامين، مطبخ صغير، غرفة معيشة، شرفة كبيرة'
                },
                {
                    'name': 'جناح رئاسي',
                    'description': 'أفخم الأجنحة مع جميع المرافق الراقية وخدمة VIP حصرية',
                    'base_price': 800.0,
                    'capacity': 2,
                    'amenities': 'تكييف، تلفزيون ذكي 65 بوصة، واي فاي مجاني، حمام فاخر مع جاكوزي، شرفة كبيرة، خدمة الغرف 24/7، خدمة كونسيرج'
                }
            ]
            
            for room_type_data in room_types_data:
                room_type = RoomType(**room_type_data)
                db.session.add(room_type)
            
            db.session.commit()
            print(f"تم إضافة {len(room_types_data)} نوع غرفة")
        
        # إنشاء الغرف إذا لم تكن موجودة
        if not Room.query.first():
            print("إضافة الغرف...")
            
            room_types = RoomType.query.all()
            room_number = 101
            
            for room_type in room_types:
                for floor in range(1, 4):  # 3 طوابق
                    for room_in_floor in range(1, 6):  # 5 غرف في كل طابق لكل نوع
                        room = Room(
                            number=str(room_number),
                            floor=floor,
                            room_type_id=room_type.id,
                            status='available',
                            description=f'غرفة رقم {room_number} - {room_type.name} في الطابق {floor}'
                        )
                        db.session.add(room)
                        room_number += 1
            
            db.session.commit()
            total_rooms = Room.query.count()
            print(f"تم إضافة {total_rooms} غرفة")
        
        # إنشاء المستخدمين التجريبيين
        print("إضافة المستخدمين التجريبيين...")
        
        # مدير النظام
        if not User.query.filter_by(username='admin').first():
            admin = User(
                username='admin',
                email='admin@hotel.com',
                first_name='مدير',
                last_name='النظام',
                phone='0501234567',
                address='الرياض، المملكة العربية السعودية',
                role='admin'
            )
            admin.set_password('admin123')
            db.session.add(admin)
        
        # موظف الاستقبال
        if not User.query.filter_by(username='reception').first():
            receptionist = User(
                username='reception',
                email='reception@hotel.com',
                first_name='موظف',
                last_name='الاستقبال',
                phone='0507654321',
                address='الرياض، المملكة العربية السعودية',
                role='receptionist'
            )
            receptionist.set_password('reception123')
            db.session.add(receptionist)
        
        # عملاء تجريبيون
        sample_customers = [
            {
                'username': 'ahmed_ali',
                'email': 'ahmed.ali@email.com',
                'first_name': 'أحمد',
                'last_name': 'علي',
                'phone': '0551234567',
                'address': 'جدة، المملكة العربية السعودية'
            },
            {
                'username': 'fatima_hassan',
                'email': 'fatima.hassan@email.com',
                'first_name': 'فاطمة',
                'last_name': 'حسن',
                'phone': '0559876543',
                'address': 'الدمام، المملكة العربية السعودية'
            },
            {
                'username': 'mohammed_salem',
                'email': 'mohammed.salem@email.com',
                'first_name': 'محمد',
                'last_name': 'سالم',
                'phone': '0555555555',
                'address': 'مكة المكرمة، المملكة العربية السعودية'
            },
            {
                'username': 'sara_omar',
                'email': 'sara.omar@email.com',
                'first_name': 'سارة',
                'last_name': 'عمر',
                'phone': '0544444444',
                'address': 'المدينة المنورة، المملكة العربية السعودية'
            }
        ]
        
        customers = []
        for customer_data in sample_customers:
            if not User.query.filter_by(username=customer_data['username']).first():
                customer = User(
                    username=customer_data['username'],
                    email=customer_data['email'],
                    first_name=customer_data['first_name'],
                    last_name=customer_data['last_name'],
                    phone=customer_data['phone'],
                    address=customer_data['address'],
                    role='customer'
                )
                customer.set_password('customer123')
                db.session.add(customer)
                customers.append(customer)
        
        db.session.commit()
        print(f"تم إضافة {len(sample_customers)} عميل تجريبي")
        
        # إنشاء حجوزات تجريبية
        print("إضافة حجوزات تجريبية...")
        
        if not Booking.query.first():
            customers = User.query.filter_by(role='customer').all()
            rooms = Room.query.limit(10).all()  # أول 10 غرف
            
            booking_count = 0
            for i, customer in enumerate(customers):
                # إنشاء 2-3 حجوزات لكل عميل
                num_bookings = random.randint(2, 3)
                
                for j in range(num_bookings):
                    if booking_count >= len(rooms):
                        break
                    
                    room = rooms[booking_count]
                    
                    # تواريخ عشوائية
                    start_date = date.today() + timedelta(days=random.randint(-30, 30))
                    end_date = start_date + timedelta(days=random.randint(1, 5))
                    
                    # حالة الحجز
                    if start_date < date.today():
                        if end_date < date.today():
                            status = 'checked_out'
                        else:
                            status = 'checked_in'
                    else:
                        status = random.choice(['confirmed', 'pending'])
                    
                    booking = Booking(
                        customer_id=customer.id,
                        room_id=room.id,
                        check_in_date=start_date,
                        check_out_date=end_date,
                        adults=random.randint(1, room.room_type.capacity),
                        children=random.randint(0, 2),
                        special_requests=f'طلب تجريبي للعميل {customer.full_name}',
                        room_rate=room.room_type.base_price,
                        status=status,
                        payment_status='paid' if status != 'pending' else 'pending'
                    )
                    
                    booking.generate_booking_number()
                    booking.calculate_total()
                    
                    db.session.add(booking)
                    db.session.flush()  # للحصول على ID الحجز
                    
                    # إنشاء دفعة إذا كان الحجز مدفوع
                    if booking.payment_status == 'paid':
                        payment = Payment(
                            booking_id=booking.id,
                            amount=booking.total_amount,
                            payment_method=random.choice(['cash', 'card', 'bank_transfer']),
                            payment_type='full',
                            status='completed',
                            notes=f'دفعة تجريبية للحجز {booking.booking_number}',
                            processed_at=datetime.utcnow()
                        )
                        payment.generate_reference()
                        db.session.add(payment)
                    
                    # تحديث حالة الغرفة
                    if status == 'checked_in':
                        room.status = 'occupied'
                    elif status == 'checked_out':
                        room.status = 'cleaning'
                    
                    booking_count += 1
            
            db.session.commit()
            print(f"تم إضافة {booking_count} حجز تجريبي")
        
        print("\n" + "="*50)
        print("تم إنشاء البيانات التجريبية بنجاح!")
        print("="*50)
        print("\nمعلومات تسجيل الدخول:")
        print("\n1. مدير النظام:")
        print("   اسم المستخدم: admin")
        print("   كلمة المرور: admin123")
        print("\n2. موظف الاستقبال:")
        print("   اسم المستخدم: reception")
        print("   كلمة المرور: reception123")
        print("\n3. العملاء التجريبيون:")
        print("   اسم المستخدم: ahmed_ali")
        print("   كلمة المرور: customer123")
        print("   (وكذلك: fatima_hassan, mohammed_salem, sara_omar)")
        print("\n" + "="*50)

if __name__ == '__main__':
    create_sample_data()
