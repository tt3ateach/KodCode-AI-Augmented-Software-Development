const tasks = JSON.parse(localStorage.getItem("tasks")) || [];
const list = document.querySelector("#task-list");
const form = document.querySelector("#quick-add-form");

function render() {
  list.innerHTML = tasks.map(task => `
    <article class="task-card">
      <h3>${task.title}</h3>
      <button onclick="toggle('${task.id}')">Done</button>
    </article>
  `).join("");
}

window.toggle = function(id) {
  const task = tasks.find(t => t.id === id);
  task.done = !task.done;
  localStorage.setItem("tasks", JSON.stringify(tasks));
  render();
};

form.addEventListener("submit", event => {
  event.preventDefault();
  tasks.push({ id: Date.now().toString(), title: event.target.title.value, done: false });
  localStorage.setItem("tasks", JSON.stringify(tasks));
  render();
});

render();
