from kool.db.models import Model, where, table


class Topic(Model):
    """These are topics that constitute a course
    
    Extends:
        Model

    """

    def __init__(self, title, **options):
        super().__init__()
        self.title = title
        self.description = options.pop('description', None)
        self.file_id = options.pop('file_id', None)


class Course(Model):
    """Course describes a plan of study for a student
    
    Extends:
        Model

    """
    
    def __init__(self, title, instructor_id, **options):
        super().__init__()
        self.title = title
        
        from kool.contrib.auth import User
        user = table(User)

        if user.get(where('_id') == str(instructor_id)):
            self.instructor_id = instructor_id
        else:
            raise ValueError('Instructor id not found!')

        self.description = options.pop('description', None)
        self.topics = []

    def __str__(self):
        return '{}'.format(self.title)

    def __repr__(self):
        return '{}'.format(self.title)

    def add_topic(self, topic_id):
        """Receives topic id, performs a query to db and
        if found, add topic id to list of topics in a given course

        :param topic_id: 

        """
        topic = table(Topic)

        if topic.get(where('_id') == str(topic_id)):
            if not topic_id in self.topics:
                self.topics.append(topic_id)
        else:
            raise ValueError('Topic id not found!')
        
        self.update()
        
        return self.topics

    def del_topic(self, topic_id):
        """Receives a topic id and deletes it from
        a list of topics for a given course

        :param topic_id: 

        """
        if topic_id in self.topics:
            self.topics.remove(topic_id)
        
        self.update()

        return self.topics
