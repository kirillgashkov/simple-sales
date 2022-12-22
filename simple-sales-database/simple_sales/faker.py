import uuid
import random
import string
import datetime


def generate_cities():
    return [
        {"id": uuid.uuid4(), "name": "Москва", "region": None},
        {"id": uuid.uuid4(), "name": "Санкт-Петербург", "region": None},
        {"id": uuid.uuid4(), "name": "Новосибирск", "region": "Новосибирская область"},
        {"id": uuid.uuid4(), "name": "Екатеринбург", "region": "Свердловская область"},
        {"id": uuid.uuid4(), "name": "Казань", "region": "Татарстан"},
        {
            "id": uuid.uuid4(),
            "name": "Нижний Новгород",
            "region": "Нижегородская область",
        },
        {"id": uuid.uuid4(), "name": "Челябинск", "region": "Челябинская область"},
        {"id": uuid.uuid4(), "name": "Красноярск", "region": "Красноярский край"},
        {"id": uuid.uuid4(), "name": "Самара", "region": "Самарская область"},
        {"id": uuid.uuid4(), "name": "Уфа", "region": "Башкортостан"},
        {"id": uuid.uuid4(), "name": "Ростов-на-Дону", "region": "Ростовская область"},
        {"id": uuid.uuid4(), "name": "Омск", "region": "Омская область"},
        {"id": uuid.uuid4(), "name": "Краснодар", "region": "Краснодарский край"},
        {"id": uuid.uuid4(), "name": "Воронеж", "region": "Воронежская область"},
        {"id": uuid.uuid4(), "name": "Пермь", "region": "Пермский край"},
        {"id": uuid.uuid4(), "name": "Волгоград", "region": "Волгоградская область"},
    ]


def generate_addresses(count, cities):
    streets = [
        "ул. Ленина",
        "ул. Кирова",
        "ул. Пушкина",
        "ул. Мира",
        "ул. Гагарина",
        "ул. Лермонтова",
        "ул. Комсомольская",
        "ул. Куйбышева",
        "ул. Ленинградская",
        "ул. Красина",
        "ул. Комсомольская",
        "ул. Куйбышева",
    ]

    return [
        {
            "id": uuid.uuid4(),
            "postal_code": str(random.randint(100000, 999999)),
            "city_id": random.choice(cities)["id"],
            "street": random.choice(streets),
            "house": str(random.randint(1, 100)),
            "apartment": str(random.randint(1, 500)),
            "note": None,
        }
        for _ in range(count)
    ]


def generate_clients(count, cities):
    adjectives = [
        "Серый",
        "Желтый",
        "Зеленый",
        "Синий",
        "Красный",
        "Белый",
        "Черный",
        "Оранжевый",
        "Фиолетовый",
    ]
    nouns = [
        "кот",
        "компьютер",
        "телефон",
        "стол",
        "стул",
    ]

    return [
        {
            "id": uuid.uuid4(),
            "organization_name": (
                "ООО "
                + "«"
                + random.choice(adjectives)
                + " "
                + random.choice(nouns)
                + "»"
            ),
            "city_id": random.choice(cities)["id"],
        }
        for _ in range(count)
    ]


last_names_for_both_genders = [
    ("Иванов", "Иванова"),
    ("Петров", "Петрова"),
    ("Сидоров", "Сидорова"),
    ("Смирнов", "Смирнова"),
    ("Михайлов", "Михайлова"),
    ("Федоров", "Федорова"),
    ("Соколов", "Соколова"),
    ("Яковлев", "Яковлева"),
    ("Попов", "Попова"),
    ("Васильев", "Васильева"),
    ("Павлов", "Павлова"),
    ("Кузнецов", "Кузнецова"),
    ("Степанов", "Степанова"),
    ("Николаев", "Николаева"),
    ("Алексеев", "Алексеева"),
    ("Александров", "Александрова"),
    ("Андреев", "Андреева"),
    ("Антонов", "Антонова"),
    ("Борисов", "Борисова"),
]
male_first_names_and_middle_names_for_both_genders = [
    ("Александр", ("Александрович", "Александровна")),
    ("Андрей", ("Андреевич", "Андреевна")),
    ("Антон", ("Антонович", "Антоновна")),
    ("Борис", ("Борисович", "Борисовна")),
    ("Вадим", ("Вадимович", "Вадимовна")),
    ("Валерий", ("Валерьевич", "Валерьевна")),
    ("Василий", ("Васильевич", "Васильевна")),
    ("Виктор", ("Викторович", "Викторовна")),
    ("Виталий", ("Витальевич", "Витальевна")),
    ("Геннадий", ("Геннадьевич", "Геннадьевна")),
    ("Георгий", ("Георгиевич", "Георгиевна")),
    ("Даниил", ("Даниилович", "Данииловна")),
    ("Денис", ("Денисович", "Денисовна")),
    ("Дмитрий", ("Дмитриевич", "Дмитриевна")),
    ("Евгений", ("Евгеньевич", "Евгеньевна")),
    ("Егор", ("Егорович", "Егоровна")),
    ("Иван", ("Иванович", "Ивановна")),
    ("Игорь", ("Игоревич", "Игоревна")),
    ("Илья", ("Ильич", "Ильна")),
    ("Кирилл", ("Кириллович", "Кирилловна")),
]
female_first_names = [
    "Александра",
    "Анна",
    "Валентина",
    "Валерия",
    "Василиса",
    "Вера",
    "Виктория",
    "Галина",
    "Дарья",
    "Евгения",
    "Екатерина",
    "Елена",
    "Ирина",
    "Ксения",
    "Лариса",
    "Мария",
]

male_last_names = [m for m, f in last_names_for_both_genders]
male_middle_names = [
    m_middle
    for m_first, (
        m_middle,
        f_middle,
    ) in male_first_names_and_middle_names_for_both_genders
]
male_first_names = [
    m_first
    for m_first, (
        m_middle,
        f_middle,
    ) in male_first_names_and_middle_names_for_both_genders
]

female_last_names = [f for m, f in last_names_for_both_genders]
female_middle_names = [
    f_middle
    for m_first, (
        m_middle,
        f_middle,
    ) in male_first_names_and_middle_names_for_both_genders
]
female_first_names = female_first_names


def generate_full_name():
    if random.choice(["male", "female"]) == "male":
        return {
            "first_name": random.choice(male_first_names),
            "middle_name": random.choice(male_middle_names),
            "last_name": random.choice(male_last_names),
        }
    else:
        return {
            "first_name": random.choice(female_first_names),
            "middle_name": random.choice(female_middle_names),
            "last_name": random.choice(female_last_names),
        }


def generate_contacts(count, clients, addresses):
    contacts = []

    for _ in range(count):
        full_name = generate_full_name()

        contacts.append(
            {
                "id": uuid.uuid4(),
                "client_id": random.choice(clients)["id"],
                "first_name": full_name["first_name"],
                "middle_name": full_name["middle_name"],
                "last_name": full_name["last_name"],
                "phone": (
                    "+7" + "".join([str(random.randint(0, 9)) for _ in range(10)])
                ),
                "email": (
                    "".join(random.choices(string.ascii_lowercase, k=10))
                    + "@example.com"
                ),
                "address_id": random.choice(addresses)["id"],
                "note": None,
            }
        )

    return contacts


def generate_contracts(count, clients, addresses):
    return [
        {
            "number": "".join([str(random.randint(0, 9)) for _ in range(10)]),
            "client_id": random.choice(clients)["id"],
            "delivery_address_id": random.choice(addresses)["id"],
            "delivery_from": (
                datetime.datetime.utcnow()
                - datetime.timedelta(days=random.randint(0, 365))
            ),
            "delivery_to": (
                datetime.datetime.utcnow()
                + datetime.timedelta(days=random.randint(0, 365))
            ),
            "warranty_from": (
                datetime.datetime.utcnow()
                - datetime.timedelta(days=random.randint(0, 365))
            ),
            "warranty_to": (
                datetime.datetime.utcnow()
                + datetime.timedelta(days=random.randint(0, 365))
            ),
            "description": None,
        }
        for _ in range(count)
    ]


def generate_product_models(count):
    return [
        {"id": uuid.uuid4(), "name": "Холодильник"},
        {"id": uuid.uuid4(), "name": "Стиральная машина"},
        {"id": uuid.uuid4(), "name": "Телевизор"},
        {"id": uuid.uuid4(), "name": "Пылесос"},
        {"id": uuid.uuid4(), "name": "Микроволновая печь"},
        {"id": uuid.uuid4(), "name": "Посудомоечная машина"},
        {"id": uuid.uuid4(), "name": "Кофеварка"},
        {"id": uuid.uuid4(), "name": "Чайник"},
        {"id": uuid.uuid4(), "name": "Электрочайник"},
        {"id": uuid.uuid4(), "name": "Электроплита"},
        {"id": uuid.uuid4(), "name": "Электроочиститель воды"},
        {"id": uuid.uuid4(), "name": "Электроочиститель воздуха"},
        {"id": uuid.uuid4(), "name": "Электрогриль"},
        {"id": uuid.uuid4(), "name": "Электрокотел"},
    ]


def generate_products(count, product_models):
    return [
        {
            "serial_number": (
                "SN" + "".join([str(random.randint(0, 9)) for _ in range(10)])
            ),
            "product_model_id": random.choice(product_models)["id"],
        }
        for _ in range(count)
    ]


def generate_contracts_products(contracts, products):
    contracts_products = []

    for contract in contracts:
        for _ in range(random.randint(1, 5)):
            contracts_products.append(
                {
                    "contract_number": contract["number"],
                    "product_serial_number": random.choice(products)["serial_number"],
                }
            )

    return contracts_products


def generate_employees(
    managers_count,
    salespeople_count,
    manager_employee_type_id,
    salesperson_employee_type_id,
    cities,
):
    employees = []

    for _ in range(managers_count):
        full_name = generate_full_name()
        employees.append(
            {
                "id": uuid.uuid4(),
                "employee_type_id": manager_employee_type_id,
                "first_name": full_name["first_name"],
                "middle_name": full_name["middle_name"],
                "last_name": full_name["last_name"],
                "city_id": random.choice(cities)["id"],
            }
        )

    for _ in range(salespeople_count):
        full_name = generate_full_name()
        employees.append(
            {
                "id": uuid.uuid4(),
                "employee_type_id": salesperson_employee_type_id,
                "first_name": full_name["first_name"],
                "middle_name": full_name["middle_name"],
                "last_name": full_name["last_name"],
                "city_id": random.choice(cities)["id"],
            }
        )

    return employees


def generate_insert_statements(data, table_name):
    statements = []

    # Check if the same column names are used in all rows
    column_names = list(data[0].keys())
    column_names_set = set(column_names)

    for row in data:
        if set(row.keys()) != column_names_set:
            raise ValueError("Not all rows have the same column names")

    value_tuples = []

    for row in data:
        values = []

        for column_name in column_names:
            value = row[column_name]

            if isinstance(value, str):
                values.append(f"'{value}'")
            elif isinstance(value, datetime.datetime):
                values.append(f"'{value.strftime('%Y-%m-%d %H:%M:%S')}'")
            elif isinstance(value, uuid.UUID):
                values.append(f"'{value}'")
            elif isinstance(value, int):
                values.append(f"{value}")
            elif value is None:
                values.append(f"NULL")
            else:
                raise ValueError(f"Unknown value type: {type(value)}")

        value_tuples.append(f"({', '.join(values)})")

    all_value_tuples = ", ".join(value_tuples)
    column_tuple = "(" + ", ".join(column_names) + ")"

    statements.append(
        f"INSERT INTO {table_name} {column_tuple} VALUES {all_value_tuples} ON CONFLICT DO NOTHING;"
    )

    return statements


def main():
    cities, cities_table = generate_cities(), "cities"
    addresses, addresses_table = generate_addresses(1000, cities), "addresses"
    clients, clients_table = generate_clients(1000, cities), "clients"
    contacts, contacts_table = generate_contacts(1000, clients, addresses), "contacts"
    product_models, product_models_table = (
        generate_product_models(1000),
        "product_models",
    )
    products, products_table = generate_products(1000, product_models), "products"
    contracts, contracts_table = (
        generate_contracts(1000, clients, addresses),
        "contracts",
    )
    contracts_products, contracts_products_table = (
        generate_contracts_products(contracts, products),
        "contracts_products",
    )

    # EmployeeTypes:
    #
    # {"id": "4cf1d446-8624-4176-9121-18c3b0cca623", "name": "manager"},
    # {"id:" "fb6b4665-556b-4a12-b7f0-333f73ca6f16", "name": "salesperson"},

    employees, employees_table = (
        generate_employees(
            10,
            100,
            "4cf1d446-8624-4176-9121-18c3b0cca623",
            "fb6b4665-556b-4a12-b7f0-333f73ca6f16",
            cities,
        ),
        "employees",
    )

    data_table_pairs = [
        (cities, cities_table),
        (addresses, addresses_table),
        (clients, clients_table),
        (contacts, contacts_table),
        (product_models, product_models_table),
        (products, products_table),
        (contracts, contracts_table),
        (contracts_products, contracts_products_table),
        (employees, employees_table),
    ]

    with open("fake_data.sql", "w") as f:
        f.write("BEGIN;\n\n")
        for data, table in data_table_pairs:
            print("Generating insert statements for table:", table)
            statements = generate_insert_statements(data, table)
            f.write("\n".join(statements) + "\n\n")
        f.write("COMMIT;\n")


if __name__ == "__main__":
    main()
