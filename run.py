#!/usr/bin/env python3
"""
ملف تشغيل تطبيق إدارة الفنادق
Hotel Management System - Main Application Runner
"""

import os
from app import create_app, db
from app.models import User, Room, RoomType, Booking, Payment

# إنشاء التطبيق
app = create_app(os.getenv('FLASK_ENV') or 'default')

@app.shell_context_processor
def make_shell_context():
    """إضافة المتغيرات لسياق Shell"""
    return {
        'db': db,
        'User': User,
        'Room': Room,
        'RoomType': RoomType,
        'Booking': Booking,
        'Payment': Payment
    }

@app.cli.command()
def init_db():
    """إنشاء قاعدة البيانات وإضافة البيانات الأولية"""
    
    print("إنشاء قاعدة البيانات...")
    db.create_all()
    
    # إنشاء أنواع الغرف الافتراضية
    if not RoomType.query.first():
        print("إضافة أنواع الغرف الافتراضية...")
        
        room_types = [
            {
                'name': 'غرفة عادية',
                'description': 'غرفة مريحة مع جميع المرافق الأساسية',
                'base_price': 200.0,
                'capacity': 2,
                'amenities': 'تكييف، تلفزيون، واي فاي مجاني، حمام خاص'
            },
            {
                'name': 'غرفة ديلوكس',
                'description': 'غرفة فاخرة مع إطلالة رائعة ومرافق متقدمة',
                'base_price': 350.0,
                'capacity': 2,
                'amenities': 'تكييف، تلفزيون ذكي، واي فاي مجاني، حمام فاخر، ميني بار، شرفة'
            },
            {
                'name': 'جناح عائلي',
                'description': 'جناح واسع مناسب للعائلات مع غرفة معيشة منفصلة',
                'base_price': 500.0,
                'capacity': 4,
                'amenities': 'تكييف، تلفزيون ذكي، واي فاي مجاني، حمامين، مطبخ صغير، غرفة معيشة'
            },
            {
                'name': 'جناح رئاسي',
                'description': 'أفخم الأجنحة مع جميع المرافق الراقية',
                'base_price': 800.0,
                'capacity': 2,
                'amenities': 'تكييف، تلفزيون ذكي، واي فاي مجاني، حمام فاخر، جاكوزي، شرفة كبيرة، خدمة الغرف 24/7'
            }
        ]
        
        for room_type_data in room_types:
            room_type = RoomType(**room_type_data)
            db.session.add(room_type)
        
        db.session.commit()
    
    # إنشاء غرف تجريبية
    if not Room.query.first():
        print("إضافة الغرف التجريبية...")
        
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
                        description=f'غرفة رقم {room_number} - {room_type.name}'
                    )
                    db.session.add(room)
                    room_number += 1
        
        db.session.commit()
    
    # إنشاء مستخدم موظف استقبال تجريبي
    if not User.query.filter_by(username='reception').first():
        print("إضافة موظف استقبال تجريبي...")
        
        receptionist = User(
            username='reception',
            email='reception@hotel.com',
            first_name='موظف',
            last_name='الاستقبال',
            role='receptionist'
        )
        receptionist.set_password('reception123')
        db.session.add(receptionist)
        db.session.commit()
    
    print("تم إنشاء قاعدة البيانات والبيانات الأولية بنجاح!")

if __name__ == '__main__':
    # يمكنك تغيير المنفذ هنا
    # مثال: port=8080 للوصول عبر http://localhost:8080
    app.run(debug=True, host='0.0.0.0', port=5000)
