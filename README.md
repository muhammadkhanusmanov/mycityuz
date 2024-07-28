## Endpoints

| Endpoint           | Method | Description                                 |
|--------------------|--------|---------------------------------------------|
| login/             | POST   | Foydalanuvchi tizimga kirishi uchun         |
| post/add/          | POST   | Yangi post qo'shish                         |
| users/             | GET    | Foydalanuvchilar ro'yxati                   |
| delete/user/       | DELETE | Foydalanuvchini o'chirish                   |
| delete/post/       | DELETE | Postni o'chirish                            |
| user/posts/        | POST   | Foydalanuvchi profilini olish               |
| list/posts/        | GET    | Postlar ro'yxatini olish                    |
| view/post/         | POST   | Postni ko'rish sonini oshirish              |
| google/login/      | POST   | Google orqali tizimga kirish                |
| google/register/   | POST   | Google orqali ro'yxatdan o'tish             |
| edit/profile/      | POST   | Foydalanuvchi profilini o'zgartirish        |
| get/post/          | POST   | Postni olish                                |
| save/post/         | PUT    | Postni saqlash                              |
| get/saveds/        | POST   | Saqlangan postlarni olish                   |

## Endpoints foydalanish

#### login/
> ##### So'rov
>> `Avtorizatsiya > Asosiy Autentifikatsiya` <br/> `Body > Yo'q`
> ##### Javob
>> `Token: str, Status: Foydalanuvchi roli`

#### post/add/
> ##### So'rov
>> `Avtorizatsiya > Token Autentifikatsiya` <br/> `Body > { 'title': str, 'branch': str, 'position': str, 'owner': int, 'description': str, 'location': str, 'pic1': file, 'pic2': file (ixtiyoriy), 'pic3': file (ixtiyoriy) }`
> ##### Javob
>> `{'id': int, 'title': str, 'branch': str, 'position': str, 'owner': int, 'description': str, 'location': str, 'pic1': str, 'pic2': str, 'pic3': str}`

#### users/
> ##### So'rov
>> `Avtorizatsiya > Token Autentifikatsiya` <br/> `Body > Yo'q`
> ##### Javob
>> `[{'id': int, 'username': str, 'email': str, 'first_name': str, 'last_name': str}]`

#### delete/user/
> ##### So'rov
>> `Avtorizatsiya > Token Autentifikatsiya` <br/> `Body > {'id': int}`
> ##### Javob
>> `{'success': bool}`

#### delete/post/
> ##### So'rov
>> `Avtorizatsiya > Token Autentifikatsiya` <br/> `Body > {'id': int}`
> ##### Javob
>> `{'success': bool}`

#### user/posts/
> ##### So'rov
>> `Avtorizatsiya > Token Autentifikatsiya` <br/> `Body > Yo'q`
> ##### Javob
>> `{'owner': {'id': int, 'username': str, 'email': str, 'first_name': str, 'last_name': str}, 'posts': [{'id': int, 'title': str, 'description': str, 'branch': str, 'owner': int}]}`

#### list/posts/
> ##### So'rov
>> `Avtorizatsiya > Token Autentifikatsiya` <br/> `Body > Yo'q`
> ##### Javob
>> `[{'id': int, 'title': str, 'description': str, 'branch': str, 'owner': int}]`

#### view/post/
> ##### So'rov
>> `Avtorizatsiya > Token Autentifikatsiya` <br/> `Body > {'id': int}`
> ##### Javob
>> `{'status': bool}`

#### google/login/
> ##### So'rov
>> `Body > {'access_token': str}`
> ##### Javob
>> `{'token': str}`

#### google/register/
> ##### So'rov
>> `Body > {'access_token': str}`
> ##### Javob
>> `{'token': str}`

#### edit/profile/
> ##### So'rov
>> `Avtorizatsiya > Token Autentifikatsiya` <br/> `Body > {'username': str, 'full_name': str, 'phone_number': str}`
> ##### Javob
>> `{'success': bool}`

#### get/post/
> ##### So'rov
>> `Avtorizatsiya > Token Autentifikatsiya` <br/> `Body > {'id': int}`
> ##### Javob
>> `{'id': int, 'title': str, 'branch': str, 'position': str, 'owner': int, 'description': str, 'location': str, 'pic1': str, 'pic2': str, 'pic3': str}`

#### save/post/
> ##### So'rov
>> `Avtorizatsiya > Token Autentifikatsiya` <br/> `Body > {'id': int}`
> ##### Javob
>> `{'status': bool, 'message': str}`

#### get/saveds/
> ##### So'rov
>> `Avtorizatsiya > Token Autentifikatsiya` <br/> `Body > Yo'q`
> ##### Javob
>> `{'id': int, 'user': int, 'posts': [{'id': int, 'title': str, 'branch': str, 'description': str}]}`
