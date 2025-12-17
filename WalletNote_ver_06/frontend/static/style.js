/* =========================
   Auth
========================= */
document.addEventListener("DOMContentLoaded", () => {

    const loginForm = document.getElementById("loginForm");
    if (loginForm) {
        loginForm.addEventListener("submit", async (e) => {
            e.preventDefault();

            const data = {
                email: loginForm.email.value,
                password: loginForm.password.value
            };

            const res = await fetch("/login", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(data)
            });

            if (res.ok) {
                location.href = "/dashboard";
            } else {
                alert("Login failed");
            }
        });
    }

    const signupForm = document.getElementById("signupForm");
    if (signupForm) {
        signupForm.addEventListener("submit", async (e) => {
            e.preventDefault();

            const data = {
                username: signupForm.username.value,
                email: signupForm.email.value,
                password: signupForm.password.value
            };

            const res = await fetch("/signup", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(data)
            });

            if (res.ok) {
                location.href = "/dashboard";
            } else {
                alert("Signup failed");
            }
        });
    }
});


/* =========================
   Dashboard View Switch
========================= */
function switchView(type, button) {
    document.querySelectorAll(".nav-btn").forEach(btn => {
        btn.classList.remove("active");
    });
    button.classList.add("active");

    document.getElementById("expenseView").classList.add("hidden");
    document.getElementById("incomeView").classList.add("hidden");

    if (type === "expense") {
        document.getElementById("expenseView").classList.remove("hidden");
    } else {
        document.getElementById("incomeView").classList.remove("hidden");
    }
}


/* =========================
   Expense Input
========================= */
async function submitExpense() {
    const date = document.getElementById("expenseDate").value;
    const service = document.getElementById("expenseService").value;
    const price = document.getElementById("expensePrice").value;

    if (!date || !service || !price) {
        alert("All fields are required");
        return;
    }

    const res = await fetch("/record/expense", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            date: date,
            service: service,
            price: price
        })
    });

    if (res.ok) {
        location.reload();
    } else {
        alert("Failed to save expense");
    }
}


/* =========================
   Income Input
========================= */
async function submitIncome() {
    const date = document.getElementById("incomeDate").value;
    const service = document.getElementById("incomeService").value;
    const price = document.getElementById("incomePrice").value;

    if (!date || !service || !price) {
        alert("All fields are required");
        return;
    }

    const res = await fetch("/record/income", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            date: date,
            service: service,
            price: price
        })
    });

    if (res.ok) {
        location.reload();
    } else {
        alert("Failed to save income");
    }
}


/* =========================
   OCR Upload
========================= */
async function submitOCR() {
    const input = document.getElementById("receiptImage");
    if (!input || !input.files.length) {
        alert("Select an image first");
        return;
    }

    const formData = new FormData();
    formData.append("image", input.files[0]);

    const res = await fetch("/record/ocr", {
        method: "POST",
        body: formData
    });

    if (res.ok) {
        location.reload();
    } else {
        alert("OCR failed");
    }
}


/* =========================
   Settings
========================= */
async function saveSettings() {
    const currency = document.getElementById("currencySelect").value;

    const res = await fetch("/setting/save", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ currency })
    });

    if (res.ok) {
        alert("Saved");
        location.href = "/dashboard";
    } else {
        alert("Failed to save settings");
    }
}


document.addEventListener("DOMContentLoaded", () => {
    loadCharts();
});

async function loadCharts() {
    await loadPieChart();
    await loadBarChart();
}

/* =========================
   Pie Chart (Income vs Expense)
========================= */
async function loadPieChart() {
    const res = await fetch("/api/chart/summary");
    if (!res.ok) return;

    const data = await res.json();

    const ctx = document.getElementById("pieChart");
    if (!ctx) return;

    new Chart(ctx, {
        type: "pie",
        data: {
            labels: ["Income", "Expense"],
            datasets: [{
                data: [data.income, data.expense],
                backgroundColor: ["#4CAF50", "#d4af37"]
            }]
        }
    });
}

/* =========================
   Bar Chart (Expense by Service)
========================= */
async function loadBarChart() {
    const res = await fetch("/api/chart/expense");
    if (!res.ok) return;

    const rows = await res.json();

    const labels = rows.map(r => r.service);
    const values = rows.map(r => r.total);

    const ctx = document.getElementById("barChart");
    if (!ctx) return;

    new Chart(ctx, {
        type: "bar",
        data: {
            labels: labels,
            datasets: [{
                label: "Expense",
                data: values,
                backgroundColor: "#d4af37"
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

