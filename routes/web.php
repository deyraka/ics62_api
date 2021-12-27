<?php

use App\Http\Controllers\DataController;

/** @var \Laravel\Lumen\Routing\Router $router */

/*
|--------------------------------------------------------------------------
| Application Routes
|--------------------------------------------------------------------------
|
| Here is where you can register all of the routes for an application.
| It is a breeze. Simply tell Lumen the URIs it should respond to
| and give it the Closure to call when that URI is requested.
|
*/

$router->get('/', function () use ($router) {
    return $router->app->version();
});
$router->get('kabko',  ['middleware' => 'cors', 'uses' => 'DataController@cat_kabko']);
$router->post('list/{id}', ['middleware' => 'cors', 'uses' => 'DataController@bs_by_kab']);
$router->post('detailbs/{bs}', ['middleware' => 'cors', 'uses' => 'DataController@bs_detail']);


//menggunakan route group prefixes
$router->group(['prefix' => 'api'], function () use ($router) {
    $router->get('index',  ['uses' => 'DataController@index']);
    // $router->get('kabko',  ['uses' => 'DataController@cat_kabko']);
    // $router->post('list/{id}', 'DataController@bs_by_kab');
    // $router->get('motor/{id}', ['uses' => 'MotorController@showOneMotor']);
    // $router->post('motor', ['uses' => 'MotorController@create']);
    // $router->delete('motor/{id}', ['uses' => 'MotorController@delete']);
    // $router->put('motor/{id}', ['uses' => 'MotorController@update']);
});
