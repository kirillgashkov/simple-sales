import axios from "./axios";
import { Employee, EmployeeType, City } from "../api/models";


export class Choice {
  constructor({ id, displayName }) {
    this.id = id;
    this.displayName = displayName;
  }
}


export async function getEmployeeTypeChoices() {
  try {
    const response = await axios.get("/employee-types");
    return response.data.map((employeeTypeJson) => {
      const employeeType = new EmployeeType(employeeTypeJson);

      let displayName = employeeType.name;
      switch (employeeType.name) {
        case "manager":
          displayName = "Менеджер";
          break;
        case "salesperson":
          displayName = "Продавец";
          break;
      }

      return new Choice({
        id: employeeType.id,
        displayName: displayName,
      });
    });
  } catch (error) {
    console.log(error);
  }
}


export async function getCityChoices() {
  try {
    const response = await axios.get("/cities");
    return response.data.map((cityJson) => {
      const city = new City(cityJson);

      let displayName;
      if (city.region) {
        displayName = `${city.name}, ${city.region}`;
      } else {
        displayName = city.name;
      }

      return new Choice({
        id: city.id,
        displayName: displayName,
      });
    });
  } catch (error) {
    console.log(error);
  }
}


export async function getAssignTaskToEmployeeChoices() {
  try {
    const response = await axios.get("/employees?choices_for=assign_task_to");
    const employees = response.data.map((employeeJson) => new Employee(employeeJson));

    const fullNameCounts = new Map();
    const fullNameCityCounts = new Map();

    function getFullName(employee) {
      let fullName;
      if (employee.middle_name) {
        fullName = `${employee.last_name} ${employee.first_name} ${employee.middle_name}`;
      } else {
        fullName = `${employee.last_name} ${employee.first_name}`;
      }

      return fullName;
    }

    function getFullNameCity(employee_1) {
      let fullNameCity;
      if (employee_1.city.region) {
        fullNameCity = `${fullName}, ${employee_1.city.name}, ${employee_1.city.region}`;
      } else {
        fullNameCity = `${fullName}, ${employee_1.city.name}`;
      }

      return fullNameCity;
    }

    employees.foreach((employee_2) => {
      const fullName_1 = getFullName(employee_2);
      const fullNameCity_1 = getFullNameCity(employee_2);

      if (fullNameCounts.has(fullName_1)) {
        fullNameCounts.set(fullName_1, fullNameCounts.get(fullName_1) + 1);
      } else {
        fullNameCounts.set(fullName_1, 1);
      }

      if (fullNameCityCounts.has(fullNameCity_1)) {
        fullNameCityCounts.set(fullNameCity_1, fullNameCityCounts.get(fullNameCity_1) + 1);
      } else {
        fullNameCityCounts.set(fullNameCity_1, 1);
      }
    });
    return employees.map((employee_5) => {
      const fullName_2 = getFullName(employee_5);
      const fullNameCity_2 = getFullNameCity(employee_5);

      if (fullNameCounts.get(fullName_2) <= 1) {
        return new Choice({
          id: employee_5.id,
          displayName: fullName_2,
        });
      }

      if (fullNameCityCounts.get(fullNameCity_2) <= 1) {
        return new Choice({
          id: employee_5.id,
          displayName: fullNameCity_2,
        });
      }

      return new Choice({
        id: employee_5.id,
        displayName: `${fullNameCity_2} (${employee_5.id})`,
      });
    });
  } catch (error) {
    console.log(error);
  }
}
