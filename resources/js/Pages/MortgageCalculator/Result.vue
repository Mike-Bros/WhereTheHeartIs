<template>
    <Card title="Mortgage Calculation Results" link="javascript:void(0);">
        <div v-if="validated">
            <p class="font-semibold mb-2">Loan Inputs Summary</p>
            <p>Home Price: ${{ validated.home_price }}</p>
            <p>Down Payment: {{ validated.down_payment_percent }}%</p>
            <p>Loan Term: {{ validated.loan_term_years }} years</p>
            <p>Interest Rate: {{ validated.interest_rate_exact }}%</p>
        </div>
        <div v-if="calculationData">
            <p class="font-semibold mb-2 mt-4">Loan Calculation Summary</p>
            <p>Monthly Payment: ${{ calculationData.monthly_payment }}</p>
            <p>Total Payment: ${{ calculationData.total_payment }}</p>
            <p>Total Interest: ${{ calculationData.total_interest }}</p>
        </div>
    </Card>
</template>

<script setup>
import Card from "@/Components/Card.vue"; // Import the Card component
import { defineProps } from "vue";

defineProps({
    validated: Object,
    calculationData: Object,
});
</script>
