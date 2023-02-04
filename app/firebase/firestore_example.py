import threading
import uuid
import random
from faker import Faker
from faker.providers import date_time, lorem, person
from google.cloud.firestore import AsyncCollectionReference, ArrayRemove

from app.firebase import firebase_client

fake = Faker()
fake.add_provider(lorem)
fake.add_provider(date_time)
fake.add_provider(person)

participant_custom_fields = {
    'ee6876b6-9a56-11ed-8fc6-9801a7adcef5': 'attachments/0cfcaaca-9a57-11ed-8fc6-9801a7adcef5.jpg',
    'ef10fb60-9a56-11ed-8fc6-9801a7adcef5': 99.4,
    'ef6ef2ec-9a56-11ed-8fc6-9801a7adcef5': 'Passionate programmer with love for fiddling with internals',
    '0cfcaaca-9a57-11ed-8fc6-9801a7adcef5': [2, 3],
}

courses = [{'id': i, 'name': f'B.Tech {i}'} for i in range(1, 11)]
communities = [
    {'name': 'IIT - Delhi', 'id': 1},
    {'name': 'IIM - Calcutta', 'id': 2},
    {'name': 'IIM - Mumbai', 'id': 3},
    {'name': 'IIIT - Hyderabad', 'id': 4},
    {'name': 'DTU', 'id': 5},
]

'database/(default)/participants/{participant_id}'
'database/(default)/participants/{participant_id}/registration_data/{participant_id}'
def _create_dummy_attendee_data():
    return {
        'email': f'test+hackathon+{uuid.uuid4().hex}@pod.ai',
        'name': fake.name(),
        'course': random.choice(courses),
        'graduation_year': random.randrange(2020, 2025),
        'registered_community': random.randrange(1, 6),
        'communities': [{'name': 'IIT - Delhi', 'id': 1}, {'name': 'IIM - Calcutta', 'id': 2}],
        "stages_data": {
            "stage_id1": {

            },
            "stage_id2": {

            }
        },
        'registration_data': {
            'school10': {
                'name': 'St. Xavier School',
                'board': {
                    'id': 8,
                    'name': 'CBSE'
                },
                'id': 34,
                'aggregation_type': 1,  # CGPA
                'max_score': 10,
                'score': 8
            },
            'school12': {
                'name': 'St. Xavier School',
                'board': {
                    'id': 8,
                    'name': 'CBSE'
                },
                'id': 34,
                'aggregation_type': 2,  # CGPA
                'max_score': 100,
                'score': 89
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


attendee_collection: AsyncCollectionReference = firebase_client.collection('joeltest')
community_attendee_collection_ref = attendee_collection.where('registered_community', '==', 2)
joel_attendee = await attendee_collection.add(_create_dummy_attendee_data())
joel_attendee_doc_id = joel_attendee[1].id
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

callback_done = threading.Event()


# Create a callback on_snapshot function to capture changes
def on_snapshot(doc_snapshot, changes, read_time):
    for doc in doc_snapshot:
        print(f'Received document snapshot: {doc.id}')
    callback_done.set()


doc_ref = db.collection(u'cities').document(u'SF')

# Watch the document
doc_watch = doc_ref.on_snapshot(on_snapshot)
