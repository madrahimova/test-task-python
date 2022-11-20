import * as http from 'http';
import fetch from 'node-fetch';
import * as fs from 'fs';

const serverHost = process.env.SERVER || 'localhost';

const getUsers = (callback) => {
  fetch( `http://${serverHost}:12345/users`, { method: 'post', insecureHTTPParser: true })
  .then(response => response.json())
  .then(json => {
    const html = `
      ${
      json.body.length ?
        json.body.map((row) =>
          `<tr>
             ${Object.values(row).map((item) => `<td>${item}</td>`).join('')}
           </tr>`).join('') :
        `<tr><td colspan="8" id="no-data">Нет данных</td></tr>`
    }`

    const index = fs.readFileSync('templates/usersTable.html').toString()
    .replace('{contents}', html);

    callback(index);
  });
}

const addUser = (callback) => {
  fetch(`http://${serverHost}:12345/regions`, { method: 'post', insecureHTTPParser: true })
  .then(response => response.json())
  .then(json => {
    const html = `
      <table
        <tr>
          <td><span class="required">*</span><label for="second_name">Фамилия</label></td>
          <td><input id="second_name" name="second_name" type="text" required/></td>
        </tr>
        <tr>
          <td><span class="required">*</span><label for="first_name">Имя</label></td>
          <td><input id="first_name" name="first_name" type="text" required/></td>
        </tr>
        <tr>
          <td><label for="patronymic">Отчество</label></td>
          <td><input id="patronymic" name="patronymic" type="text"/></td>
        </tr>
        <tr>
          <td><label for="region_id">Регион</label></td>
          <td><select id="region_id" name="region_id" oninput="selectRegion(this)">
            <option value="">-- Выберите регион --</option>
            ${json.body.length ?
              json.body.map((item) =>
                `<option value="${item['id']}">${item['region_name']}</option>`).join('')
              : ''
            }
          </select></td>
        </tr>
        <tr>
          <td><label for="city_id">Город</label></td>
          <td><select id="city_id" name="city_id">
            <option value="">-- Выберите город --</option>
          </select></td>
        </tr>
        <tr>
          <td><label for="phone">Контактный телефон</label></td>
          <td>
            <input id="phone" name="phone" type="tel" pattern="\\+[0-9]\\s[0-9]{3}\\s[0-9]{3}\\s[0-9]{2}\\s[0-9]{2}$">
            <span id="hint">Формат: +7 999 999 99 99</span>
          </td>
        </tr>
        <tr>
          <td><label for="email">e-mail</label></td>
          <td><input id="email" name="email" type="email"/></td>
        </tr>
      </table>`;

    const index = fs.readFileSync('templates/addForm.html').toString()
    .replace('{contents}', html);

    callback(index);
  });
}

const importFromFile = (contents, type = 'excel' | 'pdf', callback) => {
  fetch(`http://${serverHost}:12345/import/${type}`,
    { method: 'post', body: contents, insecureHTTPParser: true })
  .then((response => response.json()))
  .then((json => {
    if (json.body === 'OK')
      callback(200);
    else
      callback(500);
  }))
  .catch(() => callback(500));
}

const exportToFile = (type = 'excel' | 'pdf', callback) => {
  fetch(`http://${serverHost}:12345/export/${type}`, { method: 'post', insecureHTTPParser: true })
  .then(response => response.text())
  .then(contents => callback(200, contents))
  .catch(() => callback(500));
}

const writeHTML = (response, html) => {
  response.writeHeader(200, { 'Content-Type': 'text/html' });
  response.write(html);
  response.end();
}

http.createServer((request, response) => {
  let body = '';
  switch (request.url) {
    case '/':
      response.writeHeader(302, { 'Location': '/users' });
      response.end();
      break;
    case '/users':
      getUsers(html => writeHTML(response, html));
      break;
    case '/users/add':
      addUser(html => writeHTML(response, html));
      break;
    case '/import/excel':
      request.on('data', (chunk) => body += chunk);
      request.on('end', () => {
        importFromFile(body, 'excel', (code) => {
          response.writeHead(code);
          response.end();
        });
      });
      break;
    case '/export/excel':
      exportToFile('excel', (code, data) => {
        response.writeHead(code);
        if (code === 200)
            response.write(data);
        response.end();
      });
      break;
    case '/import/pdf':
      request.on('data', (chunk) => body += chunk);
      request.on('end', () => {
        importFromFile(body, 'pdf', (code) => {
          response.writeHead(code);
          response.end();
        });
      });
      break;
    case '/export/pdf':
      exportToFile('pdf', (code, data) => {
        response.writeHead(code);
        if (code === 200)
          response.write(data);
        response.end();
      });
      break;
    case '/styles.css':
      response.setHeader('Content-type', 'text/css');
      response.write(fs.readFileSync('styles.css'));
      response.end();
      break;
    default:
      response.writeHeader(200, { 'Content-Type': 'text/html' });
      response.end();
      break;
  }
}).listen(8080, () =>
  console.log(`Client is listening on http://localhost:8080`)
);