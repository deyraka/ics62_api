<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Factories\HasFactory;

class ViewRekap extends Model

{

    use HasFactory;
    
    protected $table = 'rekap_per_bs_all_new';
    protected $hidden = [];

}