export class User {
  constructor({ username, employee }) {
    this.username = username;
    this.employee = new Employee(employee);
  }
}

export class Employee {
  constructor({ id, employee_type, first_name, middle_name, last_name, city }) {
    this.id = id;
    this.employee_type = new EmployeeType(employee_type);
    this.first_name = first_name;
    this.middle_name = middle_name;
    this.last_name = last_name;
    this.city = new City(city);
  }
}

export class EmployeeType {
  constructor({ id, name }) {
    this.id = id;
    this.name = name;
  }
}

export class City {
  constructor({ id, name, region }) {
    this.id = id;
    this.name = name;
    this.region = region;
  }
}
