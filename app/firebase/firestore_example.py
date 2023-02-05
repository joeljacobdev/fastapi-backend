from random import randrange
from datetime import timedelta, datetime
import uuid
import random
from faker import Faker
from faker.providers import date_time, lorem, person
from faker_education import SchoolProvider
from google.cloud.firestore import AsyncCollectionReference, ArrayRemove

from app.firebase import setup
from main import setting

await setup.setup(setting.FIREBASE_ADMIN_CONFIG)
from app.firebase import firebase_client

fake = Faker()
fake.add_provider(lorem)
fake.add_provider(date_time)
fake.add_provider(person)
fake.add_provider(SchoolProvider)

start_date = datetime.strptime('1/1/2008 1:30 PM', '%m/%d/%Y %I:%M %p')
end_date = datetime.strptime('1/1/2023 4:50 AM', '%m/%d/%Y %I:%M %p')

participant_custom_fields = {
    'ee6876b6-9a56-11ed-8fc6-9801a7adcef5': 'attachments/0cfcaaca-9a57-11ed-8fc6-9801a7adcef5.jpg',
    'ef10fb60-9a56-11ed-8fc6-9801a7adcef5': 99.4,
    'ef6ef2ec-9a56-11ed-8fc6-9801a7adcef5': 'Passionate programmer with love for fiddling with internals',
    '0cfcaaca-9a57-11ed-8fc6-9801a7adcef5': [2, 3],
}

schools = []
for school_id in range(1, 100):
    schools.append({
        'name': fake.unique.school_name(),
        'id': school_id
    })

courses = [{'id': i, 'name': f'B.Tech {i}'} for i in range(1, 11)]
user_id = 0
stage_id = 1
stages = {}
for i in range(1, 10):
    stages[i] = [stage_id, stage_id + 1]
    stage_id = stage_id + 2

communities = [
    {'name': 'IIT - Delhi', 'id': 1},
    {'name': 'IIM - Calcutta', 'id': 2},
    {'name': 'IIM - Mumbai', 'id': 3},
    {'name': 'IIIT - Hyderabad', 'id': 4},
    {'name': 'DTU', 'id': 5},
]

'database/(default)/participants/{participant_id}'
'database/(default)/participants/{participant_id}/registration_data/{participant_id}'


def random_date():
    """
    This function will return a random datetime between two datetime
    objects.
    """
    delta = end_date - start_date
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return start_date + timedelta(seconds=random_second)


def _get_stage_custom_fields():
    return {
        f"{uuid.uuid4()}": random.randrange(1, 2000),
        f"{uuid.uuid4()}": random.randrange(1, 2000)
    }


# TODO setting field to null


def _create_dummy_attendee_data():
    global user_id
    global stages
    user_id = user_id + 1
    event_id = random.randrange(1, 10)
    stage = stages[event_id]
    user_id = user_id
    email = f'test+hackathon+{uuid.uuid4().hex}@pod.ai'
    school10 = random.choice(schools)
    school12 = random.choice(schools)
    return {
        'attendee': {
            'email': email,
            'event_id': event_id,
            'user_id': user_id,
            'status': random.randrange(1, 3),  # 1 - added, 2 - active, 3 - absent
            'name': fake.name(),
            'course': random.choice(courses),
            'graduation_year': random.randrange(2020, 2025),
            'registered_community': random.randrange(1, 6),
            'communities': [{'name': 'IIT - Delhi', 'id': 1}, {'name': 'IIM - Calcutta', 'id': 2}],
            "stages_data": {
                f'{stage[0]}': {
                    **_get_stage_custom_fields(),
                    "last_moved_in": random_date()
                },
                f'{stage[1]}': {
                    "last_moved_in": None
                }
            }
        },
        'registration_data': {
            'email': email,
            'event_id': event_id,
            'user_id': user_id,
            'school10': {
                **school10,
                'board': {
                    'id': 8,
                    'name': 'CBSE'
                },
                'aggregation_type': 1,  # CGPA
                'max_score': 20,
                'score': random.randrange(1, 21)
            },
            'school12': {
                **school12,
                'board': {
                    'id': 8,
                    'name': 'CBSE'
                },
                'aggregation_type': 2,  # Percentage
                'max_score': 100,
                'score': random.randrange(50, 100)
            },
            'professional_experience': [
                {
                    'name': 'Software Developer - Intern',
                    'company': {'id': 400, 'name': 'JTG', 'from': '2020-01-05', 'till': '2020-06-05'},
                    'description': 'Had Induction. Started with calyx project.'
                },
                {
                    'name': 'Software Developer',
                    'company': {'id': 400, 'name': 'JTG', 'from': '2020-06-06', 'till': '2021-03-31'},
                    'description': '.'
                },
            ],
            'participant_custom_fields': {
                'ee6876b6-9a56-11ed-8fc6-9801a7adcef5': f'attachments/{uuid.uuid4().hex}.jpg',
                'ef10fb60-9a56-11ed-8fc6-9801a7adcef5': 99.4,
                'ef6ef2ec-9a56-11ed-8fc6-9801a7adcef5': 'Passionate programmer with love for fiddling with internals',
                '0cfcaaca-9a57-11ed-8fc6-9801a7adcef5': [2, 3],
            }
        }
    }


async def _load_data():
    for _ in range(1, 100):
        dummy_data = _create_dummy_attendee_data()
        attendee = await attendee_collection.add(dummy_data['attendee'])
        registration_data = await attendee[1].collection('registration_data').add(dummy_data['registration_data'])


attendee_collection: AsyncCollectionReference = firebase_client.collection('joeltest')
await _load_data()
attendee_data = _create_dummy_attendee_data()
joel_attendee = await attendee_collection.add(attendee_data['attendee'])
joel_attendee_doc_ref = joel_attendee[1]
joel_attendee_doc_id = joel_attendee_doc_ref.id
joel_registration_data = await joel_attendee_doc_ref.collection('registration_data').add(
    attendee_data['registration_data'])
joel_registration_data_ref = joel_registration_data[1]

for i in range(1, 5):
    await joel_attendee_doc_ref.update({'graduation_year': 2023 + i})

# Although there is limit of 1 write on a doc per second, this runs without any issues
# 1 QPS writes per document is just the maximum limit for sustained writes that we expect to always work.
# If you do a quick burst of 5, 10, or even 50 writes in one second we can handle it by simply queuing the writes and
# executing them one by one.
# However, if you keep up high QPS to a single document over a long period of time, you'll eventually exceed the write
# queue capacity and get errors back from the API.
# ref - https://groups.google.com/g/firebase-talk/c/sXmPclfystk


# deleting parent document does not delete its sub collections documents
await joel_attendee_doc_ref.delete()

registration_data_collection_group = firebase_client.collection_group('registration_data')
# stream vs get - https://stackoverflow.com/a/65941895
registrations = registration_data_collection_group.where("event_id", "==", 2).stream()
# collection group index
async for d in registrations:
    print(d.id)

registrations = registration_data_collection_group.where("event_id", "==", 2).where("school10.score", ">", 10).stream()
# collection group composite index
async for d in registrations:
    print(d.id)

# getting sub collection directly
# /joeltest/6K5aqeQlcdR5gMWXaRx0/registration_data/c0yKz0e2ZTeIpEr4x12E
registrations_data = await firebase_client.collection('joeltest/6K5aqeQlcdR5gMWXaRx0/registration_data').get()
registrations_data = registrations_data[0]
print(registrations_data.id)

community_attendee_collection_ref = attendee_collection.where('registered_community', '==', 2)
# https://stackoverflow.com/questions/52905836/how-to-query-nested-objects-in-firestore
data = await attendee_collection.document(joel_attendee_doc_id).set(
    {'registered_community': 'IIT - Delhi'}, merge=True
)
data = await attendee_collection.document(joel_attendee_doc_id).update(
    {
        'professional_experience': ArrayRemove([{
            'name': 'Software Developer - Intern',
            'company': {'id': 400, 'name': 'JTG', 'from': '2020-01-05', 'till': '2020-06-05'},
            'description': 'Had Induction. Started with calyx project.'
        }])
    }
)

del_response = await firebase_client.collection("laptop").document('1').delete()

attendees = await attendee_collection.where('email', '==', 'joel@gmail.com').get()
attendees = await attendee_collection.where('email', 'in', ['joel@gmail.com']).get()
attendees = await attendee_collection.where('professional_experience', 'array_contains',
                                            {
                                                'name': 'Software Developer',
                                                'company': {'id': 400, 'name': 'JTG', 'from': '2020-06-06',
                                                            'till': '2021-03-31'},
                                                'description': '.'
                                            }).get()

# callback_done = threading.Event()
# Create a callback on_snapshot function to capture changes
# def on_snapshot(doc_snapshot, changes, read_time):
#     for doc in doc_snapshot:
#         print(f'Received document snapshot: {doc.id}')
#     callback_done.set()
#
#
# doc_ref = db.collection(u'cities').document(u'SF')
#
# # Watch the document
# doc_watch = doc_ref.on_snapshot(on_snapshot)
