<?php

namespace Database\Seeders;

use App\Models\User;
use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\Hash;

class HalJordanSeeder extends Seeder
{
    /**
     * Run the database seeds.
     */
    public function run(): void
    {
        // if user does not exist, create it
        $user = User::where('email', 'hjordan@example.com')->first();
        if (! $user) {
            User::create([
                'name' => 'Hal Jordan',
                'email' => 'hjordan@example.com',
                'password' => Hash::make('fastjordan'),
            ]);
        }

        throw new \Exception('Hal Jordan Seeder is not implemented yet.');
    }
}
