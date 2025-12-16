/* =====================================================
   WalletNote Frontend Controller
   ===================================================== */

const WalletNote = {

    /* ---------- Auth ---------- */

    async login() {
        const username = document.getElementById("username").value;
        const password = document.getElementById("password").value;
        const error = document.getElementById("errorMessage");

        try {
            const res = await fetch("/api/login", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({ username, password })
            });

            const data = await res.json();

            if (!res.ok || !data.success) {
                throw new Error("Invalid username or password");
            }

            window.location.href = "/dashboard";
        } catch (e) {
            error.textContent = e.message;
            error.classList.remove("hidden");
        }
    },

    async signup() {
        const username = document.getElementById("username").value;
        const email = document.getElementById("email").value;
        const password = document.getElementById("password").value;
        const error = document.getElementById("errorMessage");

        try {
            const res = await fetch("/api/signup", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({ username, email, password })
            });

            const data = await res.json();

            if (!res.ok || !data.success) {
                throw new Error(data.message || "Signup failed");
            }

            window.location.href = "/dashboard";
        } catch (e) {
            error.textContent = e.message;
            error.classList.remove("hidden");
        }
    },

    async logout() {
        await fetch("/api/logout", { method: "POST" });
        window.location.href = "/";
    },

    /* ---------- Records ---------- */

    async addRecord() {
        const date = document.getElementById("recordDate").value;
        const service = document.getElementById("service").value;
        const price = document.getElementById("price").value;

        await fetch("/api/record", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({ date, service, price })
        });

        window.location.reload();
    },

    async uploadOCR() {
        const input = document.getElementById("receiptImage");
        const result = document.getElementById("ocrResult");

        if (!input.files.length) return;

        const formData = new FormData();
        formData.append("image", input.files[0]);

        try {
            const res = await fetch("/api/ocr", {
                method: "POST",
                body: formData
            });

            const data = await res.json();

            if (!res.ok || !data.success) {
                throw new Error("OCR failed");
            }

            result.textContent =
                `Detected: ${data.service} / ${data.price} / ${data.date}`;
            result.classList.remove("hidden");

            setTimeout(() => window.location.reload(), 800);
        } catch {
            result.textContent = "OCR failed. Please try again.";
            result.classList.remove("hidden");
        }
    },

    /* ---------- Settings ---------- */

    initCurrency(currentCurrency) {
        const select = document.getElementById("currencySelect");
        if (select) select.value = currentCurrency;
    },

    async saveCurrency() {
        const currency = document.getElementById("currencySelect").value;
        const message = document.getElementById("currencyMessage");

        await fetch("/api/setting/currency", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({ currency })
        });

        message.textContent = "Currency updated.";
        message.classList.remove("hidden");
    },

    /* ---------- Graph ---------- */

    renderGraphs(data) {
        if (!data) return;

        const createLineChart = (id, label, dataset) => {
            const canvas = document.getElementById(id);
            if (!canvas) return;

            new Chart(canvas, {
                type: "line",
                data: {
                    labels: Object.keys(dataset),
                    datasets: [{
                        label,
                        data: Object.values(dataset),
                        borderColor: "#d4af37",
                        backgroundColor: "rgba(212,175,55,0.2)",
                        tension: 0.3
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: { display: false }
                    }
                }
            });
        };

        createLineChart("monthlyGraph", "Monthly", data.monthly);
        createLineChart("yearlyGraph", "Yearly", data.yearly);
        createLineChart("dailyGraph", "Daily", data.daily);
    }
};
