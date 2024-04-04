import axios from "./axios";
import { Employee, EmployeeType, City } from "../api/models";

export class Choice {
  constructor({ id, displayName }) {
    this.id = id;
    this.displayName = displayName;
  }
}

export function getEmployeeTypeChoices() {
  return axios
    .get("/employee-types")
    .then((response) => {
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
    })
    .catch((error) => {
      console.log(error);
    });
}

export function getCityChoices() {
  return axios
    .get("/cities")
    .then((response) => {
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
    })
    .catch((error) => {
      console.log(error);
    });
}

export function getAssignTaskToEmployeeChoices() {
  return axios
    .get("/employees?choices_for=assign_task_to")
    .then((response) => {
      const employees = response.data.map(
        (employeeJson) => new Employee(employeeJson)
      );

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

      function getFullNameCity(employee) {
        const fullName = getFullName(employee);

        let fullNameCity;
        if (employee.city.region) {
          fullNameCity = `${fullName}, ${employee.city.name}, ${employee.city.region}`;
        } else {
          fullNameCity = `${fullName}, ${employee.city.name}`;
        }

        return fullNameCity;
      }

      employees.foreach((employee) => {
        const fullName = getFullName(employee);
        const fullNameCity = getFullNameCity(employee);

        if (fullNameCounts.has(fullName)) {
          fullNameCounts.set(fullName, fullNameCounts.get(fullName) + 1);
        } else {
          fullNameCounts.set(fullName, 1);
        }

        if (fullNameCityCounts.has(fullNameCity)) {
          fullNameCityCounts.set(
            fullNameCity,
            fullNameCityCounts.get(fullNameCity) + 1
          );
        } else {
          fullNameCityCounts.set(fullNameCity, 1);
        }
      });

      return employees.map((employee) => {
        const fullName = getFullName(employee);
        const fullNameCity = getFullNameCity(employee);

        if (fullNameCounts.get(fullName) <= 1) {
          return new Choice({
            id: employee.id,
            displayName: fullName,
          });
        }

        if (fullNameCityCounts.get(fullNameCity) <= 1) {
          return new Choice({
            id: employee.id,
            displayName: fullNameCity,
          });
        }

        return new Choice({
          id: employee.id,
          displayName: `${fullNameCity} (${employee.id})`,
        });
      });
    })
    .catch((error) => {
      console.log(error);
    });
}
