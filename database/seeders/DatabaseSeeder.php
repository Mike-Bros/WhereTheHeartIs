<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\File;

class DatabaseSeeder extends Seeder
{
    /**
     * Seed the application's database.
     *
     * @return void
     */
    public function run()
    {
        // Get all seeder files in the database/seeders directory
        $seederFiles = File::allFiles(__DIR__);

        foreach ($seederFiles as $file) {
            // Get the seeder class name without the .php extension
            $className = pathinfo($file, PATHINFO_FILENAME);

            // Ignore the DatabaseSeeder class itself
            if ($className !== 'DatabaseSeeder') {
                // Fully qualify the class name including namespace
                $class = __NAMESPACE__.'\\'.$className;

                // Ensure that the class exists and is a subclass of Seeder
                if (class_exists($class) && is_subclass_of($class, Seeder::class)) {
                    try {
                        $this->call($class);
                    } catch (\Exception $e) {
                        $this->command->error("  Exception running seeder: $class");
                        $msg = $e->getMessage();
                        $this->command->error("  $msg");
                        $this->command->error("  $class <error>FAILED</error>");
                    }
                }
            }
        }
    }
}
