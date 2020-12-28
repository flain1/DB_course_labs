"""Create fake models for tests and seeding dev DB."""
from faker import Factory as FakerFactory
import factory
import random

from db_labs.model import Developer, Skill, Vacancy
from db_labs.model.user import NormalUser, User
from db_labs.db import db
from jetkit.db import Session

faker: FakerFactory = FakerFactory.create()
DEFAULT_NORMAL_USER_EMAIL = "test@test.test"
DEFAULT_PASSWORD = "testo"


def seed_db():
    # seed DB with factories here
    # https://pytest-factoryboy.readthedocs.io/en/latest/#model-fixture

    # default normal user
    if not User.query.filter_by(email=DEFAULT_NORMAL_USER_EMAIL).one_or_none():
        # add default user for testing
        db.session.add(
            NormalUserFactory.create(
                email=DEFAULT_NORMAL_USER_EMAIL, password=DEFAULT_PASSWORD
            )
        )
        print(
            f"Created default user with email {DEFAULT_NORMAL_USER_EMAIL} "
            f"with password '{DEFAULT_PASSWORD}'"
        )

    VacancyFactory.create_batch(10)  # Developers and skills will be created as well

    db.session.commit()
    print("Database seeded.")


class SQLAFactory(factory.alchemy.SQLAlchemyModelFactory):
    """Use a scoped session when creating factory models."""

    class Meta:
        abstract = True
        sqlalchemy_session = Session


class UserFactoryFactory(SQLAFactory):
    class Meta:
        abstract = True

    dob = factory.LazyAttribute(lambda x: faker.simple_profile()["birthdate"])
    name = factory.LazyAttribute(lambda x: faker.name())
    password = DEFAULT_PASSWORD
    avatar_url = factory.LazyAttribute(
        lambda x: f"https://placem.at/people?w=200&txt=0&random={random.randint(1, 100000)}"
    )


class NormalUserFactory(UserFactoryFactory):
    class Meta:
        model = NormalUser

    email = factory.Sequence(lambda n: f"normaluser.{n}@example.com")


class SkillFactory(SQLAFactory):
    class Meta:
        model = Skill

    name = factory.Sequence(lambda x: f"{x}-{faker.word()}")


class DeveloperFactory(SQLAFactory):
    class Meta:
        model = Developer

    first_name = factory.LazyFunction(faker.first_name)
    last_name = factory.LazyFunction(faker.last_name)

    email = factory.LazyFunction(faker.email)

    skills = factory.List([factory.SubFactory(SkillFactory) for _ in range(2)])

    birthdate = factory.LazyFunction(faker.past_date)


class VacancyFactory(SQLAFactory):
    class Meta:
        model = Vacancy

    title = factory.Sequence(lambda x: f"{x}-{faker.word()}")

    developers = factory.List([factory.SubFactory(DeveloperFactory) for _ in range(5)])
