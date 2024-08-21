<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Inertia\Inertia;

class MortgageCalculatorController extends Controller
{
    public function index()
    {
        return Inertia::render('MortgageCalculator/Index');
    }

    public function calculate(Request $request)
    {
        $validated = $request->validate([
            'home_price' => 'required|numeric|min:1',
            'down_payment_percent' => 'required|numeric|min:0|max:100',
            'loan_term_years' => 'required|numeric|min:1',
            'interest_rate_exact' => 'required|numeric|min:0',
            'interest_rate_start' => 'required|numeric|min:0',
            'interest_rate_end' => 'required|numeric|min:0|gte:interest_rate_start',
            'interest_rate_step' => 'required|numeric|min:0.01',
            'cash_savings' => 'required|numeric|min:0',
            'moving_cost' => 'required|numeric|min:0',
            'closing_cost_estimation' => 'required|numeric|min:0|max:100',
        ]);

        // Perform your calculations here...
        $monthlyPayment = $validated['home_price'] * 0.01;
        $calculationData = [
            'monthly_payment' => $monthlyPayment,
            'total_payment' => $monthlyPayment * $validated['loan_term_years'] * 30,
            'total_interest' => $monthlyPayment * $validated['loan_term_years'] * 30 * 0.1,
            '',
        ];

        // Return the validated data and calculation result to the view
        return Inertia::render('MortgageCalculator/Index', [
            'data' => $validated,
            'calculationData' => $calculationData,
            'validationResults' => ['asdfasdf'],
        ]);
    }
}
