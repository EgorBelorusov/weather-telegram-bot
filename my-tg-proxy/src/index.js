export default {
  async fetch(request) {
    const url = new URL(request.url);
    // Меняем хост на api.telegram.org, сохраняя путь и параметры
    url.hostname = "api.telegram.org";

    // Создаём новый запрос к Telegram
    const modifiedRequest = new Request(url, {
      method: request.method,
      headers: request.headers,
      body: request.body,
      redirect: 'follow'
    });

    // Отправляем запрос и возвращаем ответ
    return fetch(modifiedRequest);
  }
}
