<script setup xmlns="http://www.w3.org/1999/html">
import { Head, Link } from "@inertiajs/vue3";
import Card from "@/Components/Card.vue";

defineProps({
    canLogin: {
        type: Boolean,
    },
    canRegister: {
        type: Boolean,
    },
    laravelVersion: {
        type: String,
        required: true,
    },
    phpVersion: {
        type: String,
        required: true,
    },
    logoUrl: {
        type: String,
        required: true,
    },
});

function handleImageError() {
    document.getElementById("screenshot-container")?.classList.add("!hidden");
    document.getElementById("docs-card")?.classList.add("!row-span-1");
    document.getElementById("docs-card-content")?.classList.add("!flex-row");
    document.getElementById("background")?.classList.add("!hidden");
}
</script>

<template>
    <Head title="Welcome" />
    <div class="bg-gray-50 text-black/50 dark:bg-black dark:text-white/50">

        <div
            class="relative min-h-screen flex flex-col items-center justify-center selection:bg-[#FF2D20] selection:text-white"
        >
            <div class="relative w-full max-w-2xl px-6 lg:max-w-7xl">
                <header class="grid grid-cols-2 items-center gap-2 py-10 lg:grid-cols-3">
                    <div class="flex lg:justify-center lg:col-start-2">
                        <img
                            :src="logoUrl"
                            alt="Laravel"
                            class="w-32 h-32 lg:w-40 lg:h-40"
                        />
                    </div>
                    <nav v-if="canLogin" class="-mx-3 flex flex-1 justify-end">
                        <Link
                            v-if="$page.props.auth.user"
                            :href="route('dashboard')"
                            class="rounded-md px-3 py-2 text-black ring-1 ring-transparent transition hover:text-black/70 focus:outline-none focus-visible:ring-[#FF2D20] dark:text-white dark:hover:text-white/80 dark:focus-visible:ring-white"
                        >
                            Dashboard
                        </Link>

                        <template v-else>
                            <Link
                                :href="route('login')"
                                class="rounded-md px-3 py-2 text-black ring-1 ring-transparent transition hover:text-black/70 focus:outline-none focus-visible:ring-[#FF2D20] dark:text-white dark:hover:text-white/80 dark:focus-visible:ring-white"
                            >
                                Log in
                            </Link>

                            <Link
                                v-if="canRegister"
                                :href="route('register')"
                                class="rounded-md px-3 py-2 text-black ring-1 ring-transparent transition hover:text-black/70 focus:outline-none focus-visible:ring-[#FF2D20] dark:text-white dark:hover:text-white/80 dark:focus-visible:ring-white"
                            >
                                Register
                            </Link>
                        </template>
                    </nav>
                </header>

                <main class="mt-6 grid gap-8 lg:grid-cols-3">
                    <!-- Overview Card -->
                    <Card title="Overview" link="#overview" class="lg:col-span-2">
                        <p>"Where The Heart Is" is a Laravel-based web application designed to help users explore and
                            visualize various mortgage scenarios. Users can input different mortgage conditions and
                            visualize the impact of varying interest rates and loan terms on monthly payments in
                            real-time.</p>

                        <br>
                        <!-- Usage Card -->
                        <Card title="Usage" link="#usage" class="lg:col-span-2">
                            <p>Upon loading the application, you will be presented with a clean and simple interface to
                                input mortgage details such as loan amount, interest rate, and loan term. Adjust the
                                parameters to see real-time updates in the graphs and charts, helping you analyze
                                different
                                financial scenarios.</p>
                        </Card>
                    </Card>

                    <!-- Features Card -->
                    <Card title="Features" link="#features">
                        <ul class="list-disc ml-4">
                            <li>Intuitive Interface: Clean and straightforward interface for inputting mortgage
                                details.
                            </li>
                            <li>Real-Time Visualization: Dynamic graphs and charts update in real-time.</li>
                            <li>Customizable Options: Explore different home buying scenarios.</li>
                            <li>Responsive Design: Seamless experience across devices.</li>
                            <li>Exportable Reports: Generate and export summary reports.</li>
                        </ul>
                    </Card>

                    <!-- Installation Card -->
                    <Card title="Installation and Setup" link="#installation" class="lg:col-span-2">
                        <ol class="list-decimal ml-4">
                            <li>Clone the repository and navigate into the project directory.</li>
                            <li>Use your preferred method of starting a development server. I used Laravel Herd to start
                                and develop the project.
                            </li>
                            <li>Access the app at your configured URL like:
                                <code>https://where-the-heart-is.test/</code>.
                            </li>
                            <li>Register an account or log in with a guest account.</li>
                        </ol>
                    </Card>

                    <!-- Nested Guest Account Card -->
                    <Card title="Guest Account" link="#guest-account">
                        <p>To access the application as a guest, you can use the following credentials:</p>
                        <ul class="list-disc ml-4">
                            <li>Email: <code>hjordan@example.com</code></li>
                            <li>Password: <code>fastjordan</code></li>
                        </ul>
                    </Card>
                </main>
            </div>
        </div>
    </div>
</template>
