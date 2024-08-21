<script setup>
import { ref, watch } from "vue";
import axios from "axios";
import AuthenticatedLayout from "@/Layouts/AuthenticatedLayout.vue";
import InputError from "@/Components/InputError.vue";
import InputLabel from "@/Components/InputLabel.vue";
import PrimaryButton from "@/Components/PrimaryButton.vue";
import TextInput from "@/Components/TextInput.vue";
import { Head, useForm, usePage } from "@inertiajs/vue3";
import Result from "@/Pages/MortgageCalculator/Result.vue";

const page = usePage();
const form = useForm({
    home_price: page.props.data?.home_price || 300000,
    down_payment_percent: page.props.data?.down_payment_percent || 20,
    loan_term_years: page.props.data?.loan_term_years || 30,
    interest_rate_exact: page.props.data?.interest_rate_exact || 3.5,
    interest_rate_start: page.props.data?.interest_rate_start || 3.0,
    interest_rate_end: page.props.data?.interest_rate_end || 5.0,
    interest_rate_step: page.props.data?.interest_rate_step || 0.25,
    cash_savings: page.props.data?.cash_savings || 50000,
    moving_cost: page.props.data?.moving_cost || 2000,
    closing_cost_estimation: page.props.data?.closing_cost_estimation || 3.0,
});

let cancelTokenSource = null;
const validated = ref({});
const calculationData = ref({});
const pinnedResults = ref([]);

const submit = () => {
    // If a previous request exists, cancel it
    if (cancelTokenSource) {
        cancelTokenSource.cancel("Request canceled due to a new request.");
    }

    // Create a new cancel token
    cancelTokenSource = axios.CancelToken.source();

    console.debug("Submitting calculate request", form.data());
    form.post(route("mortgage-calculator.calculate"), {
        preserveState: true,
        preserveScroll: true, // Preserve the scroll position
        cancelToken: cancelTokenSource.token, // Attach the cancel token here
        onSuccess: () => {
            console.debug("Response", usePage().props);
            calculationData.value = usePage().props.calculationData;
        },
        onError: () => {
            console.error("Error", usePage().props);
            calculationData.value = {};
        },
        onFinish: () => {
            cancelTokenSource = null;
            validated.value = usePage().props.data;
        },
    });
};

const cancelCurrentRequest = () => {
    if (cancelTokenSource) {
        cancelTokenSource.cancel("Request canceled by the user.");
        cancelTokenSource = null;
    }
};

const pinResult = () => {
    console.debug("Pinning result", calculationData.value, validated.value);
    let result = {
        ...calculationData.value,
        ...validated.value,
    };
    pinnedResults.value.push(result);
};

const saveResult = () => {
    console.debug("Saving result", pinnedResults.value);
    // TODO: Save the pinned results to the database for the user
    // Alert the user this feature is not yet implemented
    alert("Saving results to the user is not yet implemented.");
};

// Automatically submit form when any input changes
watch(
    () => form.data(),
    () => {
        submit();
    },
    { deep: true }, // Watch nested changes
);
</script>

<template>
    <AuthenticatedLayout>
        <Head title="Mortgage Calculator" />

        <div
            :class="['grid gap-8 p-6 mx-auto', pinnedResults.length ? 'grid-cols-1 lg:grid-cols-2 max-w-7xl' : 'grid-cols-1 max-w-4xl']">
            <!-- Left Column: Calculator -->
            <div class="dark:bg-gray-800 dark:text-gray-300 shadow-lg rounded-lg p-6">
                <h2 class="text-2xl font-semibold mb-4">Mortgage Calculator</h2>
                <form @submit.prevent="submit">
                    <!-- Home Price -->
                    <div class="mb-4">
                        <InputLabel for="home_price" value="Home Price" />
                        <TextInput
                            id="home_price"
                            type="number"
                            class="mt-1 block w-full"
                            v-model.number="form.home_price"
                            required
                        />
                        <InputError class="mt-2" :message="form.errors.home_price" />
                    </div>

                    <!-- Down Payment Percentage -->
                    <div class="mb-4">
                        <InputLabel for="down_payment_percent" value="Down Payment (%)" />
                        <TextInput
                            id="down_payment_percent"
                            type="number"
                            class="mt-1 block w-full"
                            v-model.number="form.down_payment_percent"
                            required
                        />
                        <InputError class="mt-2" :message="form.errors.down_payment_percent" />
                    </div>

                    <!-- Loan Term (Years) -->
                    <div class="mb-4">
                        <InputLabel for="loan_term_years" value="Loan Term (Years)" />
                        <TextInput
                            id="loan_term_years"
                            type="number"
                            class="mt-1 block w-full"
                            v-model.number="form.loan_term_years"
                            required
                        />
                        <InputError class="mt-2" :message="form.errors.loan_term_years" />
                    </div>

                    <!-- Interest Rate (Exact) -->
                    <div class="mb-4">
                        <InputLabel for="interest_rate_exact" value="Interest Rate (Exact)" />
                        <TextInput
                            id="interest_rate_exact"
                            type="number"
                            step="0.01"
                            class="mt-1 block w-full"
                            v-model.number="form.interest_rate_exact"
                            required
                        />
                        <InputError class="mt-2" :message="form.errors.interest_rate_exact" />
                    </div>

                    <!-- Interest Rate Range -->
                    <div class="grid grid-cols-3 gap-4 mb-4">
                        <div>
                            <InputLabel for="interest_rate_start" value="Rate Start" />
                            <TextInput
                                id="interest_rate_start"
                                type="number"
                                step="0.01"
                                class="mt-1 block w-full"
                                v-model.number="form.interest_rate_start"
                                required
                            />
                            <InputError class="mt-2" :message="form.errors.interest_rate_start" />
                        </div>
                        <div>
                            <InputLabel for="interest_rate_end" value="Rate End" />
                            <TextInput
                                id="interest_rate_end"
                                type="number"
                                step="0.01"
                                class="mt-1 block w-full"
                                v-model.number="form.interest_rate_end"
                                required
                            />
                            <InputError class="mt-2" :message="form.errors.interest_rate_end" />
                        </div>
                        <div>
                            <InputLabel for="interest_rate_step" value="Rate Step" />
                            <TextInput
                                id="interest_rate_step"
                                type="number"
                                step="0.01"
                                class="mt-1 block w-full"
                                v-model.number="form.interest_rate_step"
                                required
                            />
                            <InputError class="mt-2" :message="form.errors.interest_rate_step" />
                        </div>
                    </div>

                    <!-- Cash Savings -->
                    <div class="mb-4">
                        <InputLabel for="cash_savings" value="Cash Savings" />
                        <TextInput
                            id="cash_savings"
                            type="number"
                            class="mt-1 block w-full"
                            v-model.number="form.cash_savings"
                            required
                        />
                        <InputError class="mt-2" :message="form.errors.cash_savings" />
                    </div>

                    <!-- Moving Costs -->
                    <div class="mb-4">
                        <InputLabel for="moving_cost" value="Moving Costs" />
                        <TextInput
                            id="moving_cost"
                            type="number"
                            class="mt-1 block w-full"
                            v-model.number="form.moving_cost"
                            required
                        />
                        <InputError class="mt-2" :message="form.errors.moving_cost" />
                    </div>

                    <!-- Closing Cost Estimation -->
                    <div class="mb-4">
                        <InputLabel for="closing_cost_estimation" value="Closing Cost Estimation (%)" />
                        <TextInput
                            id="closing_cost_estimation"
                            type="number"
                            step="0.01"
                            class="mt-1 block w-full"
                            v-model.number="form.closing_cost_estimation"
                            required
                        />
                        <InputError class="mt-2" :message="form.errors.closing_cost_estimation" />
                    </div>

                    <!--                    <PrimaryButton class="w-full" :class="{ 'opacity-25': form.processing }"-->
                    <!--                                   :disabled="form.processing">-->
                    <!--                        Calculate-->
                    <!--                    </PrimaryButton>-->
                </form>

                <!-- Conditional Results Display -->
                <div v-if="Object.keys(calculationData).length && Object.keys(validated).length" class="mt-8">
                    <!-- Button to pin the result -->
                    <div class="float-end p-4">
                        <PrimaryButton @click="pinResult" class="">Pin Result</PrimaryButton>
                    </div>
                    <Result :validated="validated" :calculation-data="calculationData" />
                </div>
            </div>

            <!-- Right Column: Pinned Results -->
            <div v-if="pinnedResults.length > 0" class="dark:bg-gray-800 dark:text-gray-300 shadow-lg rounded-lg p-6">
                <h3 class="text-2xl font-semibold mb-4">Pinned Results</h3>
                <div v-for="(result, index) in pinnedResults" :key="index"
                     class="bg-white dark:bg-gray-800 p-4 shadow-lg rounded-lg">
                    <!-- Button to save the result -->
                    <div class="float-end p-4">
                        <PrimaryButton @click="saveResult">Save Result</PrimaryButton>
                    </div>
                    <result :validated="result" :calculation-data="result" />
                </div>
            </div>
        </div>
    </AuthenticatedLayout>
</template>

