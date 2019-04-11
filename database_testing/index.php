<!DOCTYPE html>
<html>
    <head>
    	<title>Database Testing Results</title>
	<link rel="stylesheet" type="text/css" href="/database_testing/css/style.css"/>
	<?php
	    function read_from_csv($table_name, $file_path, $reports_col_num) {
		echo "<h2>$table_name</h2>";
		echo "<table>";
		$row = 0;
		if (($handle = fopen($file_path, "r")) !== FALSE) {
		    while (($data = fgetcsv($handle, 1000, "|")) !== FALSE) {
	         	$num = count($data);
			echo "<tr>";
		        for ($c = 0; $c < $num; $c++) {
			    if ($row != 0 && $c == $reports_col_num) {
					$cell = "<a href=\"$data[$c]\">View</a>";
			    } else {
					$cell = $data[$c];
			    }
			    if ($row == 0) {
			        echo "<th>" . $cell . "</th>";
			    } else {
			        echo "<td>" . $cell . "</td>";
		            }
			}
			echo "</tr>";
		        $row++;
		    }
		    fclose($handle);
		}
		echo "</table>";
	    }
	?>
    </head>

    <body>
	<div id="header">
	    <a href="/database_testing/index.php"><img src="/database_testing/resources/logo_orange-white_DTM.svg"></a>
	    <span id="dtm_tagline">Data Warehouse Virtualization</span>
	</div>
	<div id="content">
	    <h1>Database Testing results</h1>
		<?php
			$dirs = array_filter(glob('reports/*'), 'is_dir');
			foreach ($dirs as $dir) {
				$dir = basename($dir);
				$title = ucwords(str_replace('_', ' ', $dir));
				$csv__file_path = "src/" . $dir . ".csv";
				read_from_csv($title, $csv__file_path, 8);
			}
		?>
	</div>
	<div id="footer">
	</div>
    </body>
</html>
