from google.cloud.firestore import AsyncCollectionReference, ArrayRemove

from app.firebase import firebase_client

participant_custom_fields = {
    'ee6876b6-9a56-11ed-8fc6-9801a7adcef5': 'attachments/0cfcaaca-9a57-11ed-8fc6-9801a7adcef5.jpg',
    'ef10fb60-9a56-11ed-8fc6-9801a7adcef5': 99.4,
    'ef6ef2ec-9a56-11ed-8fc6-9801a7adcef5': 'Passionate programmer with love for fiddling with internals',
    '0cfcaaca-9a57-11ed-8fc6-9801a7adcef5': [2, 3],
}

attendee_collection: AsyncCollectionReference = firebase_client.collection('attendee')
joel_attendee = await attendee_collection.add({
    'email': 'joel@gmail.com',
    'name': 'Joel Jacob',
    'course': {
        'name': 'B. Tech - CSE',
        'id': 1,
    },
    'graduation_year': 2023,
    'registered_community': None,
    'communities': [{'name': 'IIT - Delhi', 'id': 1}, {'name': 'IIM - Calcutta', 'id': 2}],
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
        'ee6876b6-9a56-11ed-8fc6-9801a7adcef5': 'attachments/0cfcaaca-9a57-11ed-8fc6-9801a7adcef5.jpg',
        'ef10fb60-9a56-11ed-8fc6-9801a7adcef5': 99.4,
        'ef6ef2ec-9a56-11ed-8fc6-9801a7adcef5': 'Passionate programmer with love for fiddling with internals',
        '0cfcaaca-9a57-11ed-8fc6-9801a7adcef5': [2, 3],
    }
})
joel_attendee_doc_id = joel_attendee[1].id
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
