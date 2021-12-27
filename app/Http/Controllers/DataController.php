<?php

namespace App\Http\Controllers;


use App\Models\Datas; //File Model
use App\Models\ViewRekap; //File Model

use Illuminate\Http\Request;
use Illuminate\Support\Facades\DB;

class DataController extends Controller
{
    /**
     * Create a new controller instance.
     *
     * @return void
     */
    public function __construct()
    {
        //
    }

    public function index()

    {

        $data = Datas::all();

        return response($data);

    }

    public function cat_kabko()

    {

        // $data = DB::select("SELECT DISTINCT kabko, kabko FROM data");
        // $data = DB::table('data')->select('kabko','kabko as name')->distinct()->get();
        $data = Datas::select('kabko as id_kabko', 'kabko as name')->distinct('kabko')->get();
        return response()->json($data, 200);

    }

    public function bs_by_kab($id)

    {

        $id_decode = urldecode($id);
        $data = ViewRekap::where('kabko', 'LIKE', '%'.$id_decode.'%')->get();
        return response()->json($data, 200);

    }

    public function bs_detail($bs)

    {

        $data = Datas::select('kode_identitas', 'kec', 'keldes', 'nama_kk', 'status')->where('kode_bs', 'LIKE', '%'.$bs.'%')->get();
        return response()->json($data, 200);

    }

    public function show($id)

    {

        $data = Datas::where('id', $id)->get();

        return response($data);

    }

    public function store(Request $request)

    {
        //we do not need this function in this app
    }

    public function update(Request $request, $id)

    {

        //we do not need this function in this app
    }

    public function destroy($id)

    {   
        //we do not need this function in this app
    }
}
