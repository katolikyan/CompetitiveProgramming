#!/usr/bin/php
<?php

#the general idea flow of this is
#		make the query url for the data that you want to grab
#		json_decode() the responce to get a php variable
#		then loop through each array in the array until you get the id you want
#		then make a variable of that and return it

# todo
# function to grab routes along path ,
# let user pick which station to start // end at when multiple return results
# do the fun part of the project ie (the routeing algorythm)
class navitia_query
{
	private		$base_url = 'https://api.navitia.io/v1/coverage/fr-idf/';
	private		$base = 'https://api.navitia.io/v1/coord';

	# fill me in
	# please don't kill my token :{
	private		$auth_token = '66d766fa-4408-4dfd-be38-21e851a208cb';
	# is this the right syntax ?

	#goes through the array of arrays
	private function nearest_s(array $data)
	{
		$cords = array();
		$tmp = $data['places'];
		$i = 0;
		while ($i < sizeof($tmp))
		{
			$flag = 0;
			if ($tmp[$i]['embedded_type'] === 'stop_area')
			{
				$tmp1 = $tmp[$i]['stop_area']['commercial_modes'];
				if (isset($tmp1))
				{
					$j = 0;
					$tmp2 = $tmp[$i]['stop_area']['commercial_modes'];
					while ($j < sizeof($tmp2))
					{
						if ($tmp2[$j]['name'] == 'Métro')
							$flag = 1;
						$j++;
					}
				}
				if ($flag == 1)
				{
					$cords[] = array('label' => $tmp[$i]['stop_area']['label'],
						'id' => $tmp[$i]['stop_area']['id']);
				}
			}
			$i++;
		}
		return ($cords);
	}

	private function make_api_query(string $url)
	{
		$qu = $this->calc_query_url($url);
		echo $qu;
		echo "\n";
		$cu = curl_init();
		curl_setopt($cu, CURLOPT_URL, $qu);
		curl_setopt($cu, CURLOPT_USERPWD, $this->auth_token);
		#curl return string instead
		curl_setopt($cu, CURLOPT_RETURNTRANSFER, true);
		$out = curl_exec($cu);
#for testing we can cache the file
		#$out = file_get_contents('test.json');
		curl_close($cu);
		#return an array instead of the object
		return json_decode($out, true);
	}

	# hey look it's strjoin
	# adds the query component to the base url
	private function calc_query_url($url)
	{
		return $this->base_url . $url;
	}

	public function get_departure_time_stop_area($stop_area)
	{
		$dt = new DateTime('now');
		$qu = "https://api.navitia.io/v1/coverage/fr-idf/networks/network%3A0%3A439/stop_areas/" .$stop_area . "/departures?count=100&from_datetime=" . $dt->format('c');
		echo $qu . "\n";
		$cu = curl_init();
		curl_setopt($cu, CURLOPT_URL, $qu);
		curl_setopt($cu, CURLOPT_USERPWD, $this->auth_token);
		curl_setopt($cu, CURLOPT_RETURNTRANSFER, true);
		$out = curl_exec($cu);
		curl_close($cu);
		file_put_contents('tmp_stop_point_depart_time.json', $out);
	}

	public function get_metro_wgs84($place1)
	{
		##
		#
		exit("coords not implemented yet");
		#
		##
		$qu = $this->base . "/" . $place1;

		$cu = curl_init();
		curl_setopt($cu, CURLOPT_URL, $qu);
		curl_setopt($cu, CURLOPT_USERPWD, $this->auth_token);
		curl_setopt($cu, CURLOPT_RETURNTRANSFER, true);
		$out = curl_exec($cu);
		curl_close($cu);
		$return_v = json_decode($out, true);
		$j = $return_v['address']['label'];
		if (substr_count($j, "(Paris)") == 1)
		{
			$tmp = substr_replace($j, "", -7);
			echo $tmp . "\n";
			return ($this->get_metro(preg_replace("/[\s]+/", '%', trim($tmp))));
		}
		else
			exit("not found in paris");
	}

	private function get_route_departures($route_code)
	{
		$qu = "https://api.navitia.io/v1/coverage/fr-idf/routes/" . $route_code . "/departures?";
		echo $qu . "\n";
		if (!file_exists('tmp_depart' . $route_code . '.json'))
		{
			$cu = curl_init();
			curl_setopt($cu, CURLOPT_URL, $qu);
			curl_setopt($cu, CURLOPT_USERPWD, $this->auth_token);
			curl_setopt($cu, CURLOPT_RETURNTRANSFER, true);
			$out = curl_exec($cu);
			curl_close($cu);
			file_put_contents('tmp_depart' . $route_code . '.json', $out);
		}
		else
			echo $route_code . 'route.json already exists';
		return ;
	}

	private function get_route_arrival($route_code)
	{
		$qu = "https://api.navitia.io/v1/coverage/fr-idf/routes/" . $route_code . "/arrivals?";
		echo $qu . "\n";
		if (!file_exists('tmp_arrival' . $route_code . '.json'))
		{
			$cu = curl_init();
			curl_setopt($cu, CURLOPT_URL, $qu);
			curl_setopt($cu, CURLOPT_USERPWD, $this->auth_token);
			curl_setopt($cu, CURLOPT_RETURNTRANSFER, true);
			$out = curl_exec($cu);
			curl_close($cu);
			file_put_contents('tmp_arrival' . $route_code . '.json', $out);
		}
		else
			echo $route_code . 'route.json already exists';
		return ;
	}

	public function get_all_routes()
	{
		$qu = "https://api.navitia.io/v1/coverage/fr-idf/networks/network:0:439/routes?depth=3&disable_geojson=true&count=50";
		echo $qu . "\n";
		if (!file_exists('tmp_all_rout_info.json'))
		{
			$cu = curl_init();
			curl_setopt($cu, CURLOPT_URL, $qu);
			curl_setopt($cu, CURLOPT_USERPWD, $this->auth_token);
			curl_setopt($cu, CURLOPT_RETURNTRANSFER, true);
			$out = curl_exec($cu);
			curl_close($cu);
			$tmp_arr = json_decode($out, true);
			$ret = $tmp_arr['routes'];
			$my_route_stop_points = array();
			foreach ($ret as $i)
			{
				foreach ($i['stop_points'] as $stop)
				{
					$my_route_stop_points[$i['id']][] = array('label' => $stop['stop_area']['label'],
						'id' => $stop['id']);
				}
#				$this->get_route_departures($i['id']);
#				$this->get_route_arrival($i['id']);
			}
			file_put_contents('tmp_semi_parsed_stop_points.json', json_encode($my_route_stop_points));
			file_put_contents('tmp_all_rout_info.json', json_encode($ret));
		}
		else
			echo 'the route json already exists';
	}

	#get metro station
	public function get_metro($place1)
	{
		$query = 'places?q=' . $place1 . '&type[stoppoint]=address';
		$return_v = $this->make_api_query($query);
		#return a nearby metro station
		return $this->nearest_s($return_v);
	}
}

$len = count($argv);
if ($len == 3)
{
	if (strlen($argv[1]) > 0 && strlen($argv[2]) > 0)
	{
		$cl = new navitia_query();
		#check if name || geo location
		if (preg_match("/(\d)+[.](\d)+[;](\d)+[.](\d)+/", $argv[1]))
		{
			#		$station_start = $cl->get_metro_wgs84($argv[1]);
			exit("wgs84 location not supported yet");
		}
		else
			$station_start = $cl->get_metro(preg_replace("/[\s]+/", '%', trim($argv[1])));
		$station_final = $cl->get_metro(preg_replace("/[\s]+/", '%', trim($argv[2])));
		##
		#
	#	echo "station start == ";
	#	print_r($station_start);
	#	echo "\n";
	#	echo "station final == ";
	#	print_r($station_final);
		#
		##
	#	if (file_exists("tmp_semi_parsed_stop_points.json"))	
		if (0)
			;
		else
		{
			$cl->get_all_routes("");
			file_put_contents('tmp_start.json', json_encode($station_start));
			file_put_contents('tmp_final.json', json_encode($station_final));
		}
		$tmp = json_decode(file_get_contents('tmp_start.json'), true);
		$tmp1 = $tmp[0]['id'];
		$depart = $cl->get_departure_time_stop_area($tmp1);
#		$cl->get_network_arivals();
#		$cl->get_network_departures();
	}
	else
		echo "please input two valid strings";
}
else if ($len == 2)
{
	echo "Not implemented yet :: single query";
}
?>
