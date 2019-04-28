<!DOCTYPE html>
<html>
	<head>
		<title>Database Testing Results</title>
		<link rel="stylesheet" type="text/css" href="/database_testing/css/style.css"/>
		<?php
			function get_images($title, $path) {
				$dirs = glob($path, GLOB_ONLYDIR);
				foreach($dirs as $val) {
					$files = glob($val.'/*.{jpg,png,gif}', GLOB_BRACE);
					if (count($files) != 0) {
						echo "<h1>$title</h1>";
						foreach($files as $file) {
							$filename = pathinfo($file)['filename'];
							echo "<div class=\"image\">";
							if (strpos($filename, 'perfmon') !== false) {
								$start = strpos($filename, '_');
								$end = strrpos($filename, '_');
								$chart_name = substr($filename, $start + 1, $end - $start);
								$subtitle = strtoupper(implode(" ", explode("_", $chart_name)));
								echo "<h3>$subtitle</h3>";
								echo "<p>   127.0.0.1 - TestBox</p>";
								echo "<p>37.252.70.55 - Teradata</p>";
							}
							echo "<a href='".$file."' ><img src='" . $file . "'></a></div>";
						}
					}
				}
			}
		?>
	</head>

	<body>
		<div id="header">
			<a href="/database_testing/index.php"><img src="/database_testing/resources/logo_orange-white_DTM.svg"></a>
			<span id="dtm_tagline">Data Warehouse Virtualization</span>
		</div>
		<div id="content">
			<?php get_images("Latency / TPS curve", "."); ?>
			<?php get_images("PerfMon Metrics Reports", "./perfmon_report"); ?>
			<h1>JMeter Dashboard Report</h1>
			<iframe src="./dashboard_report/index.html" width="100%" height="1350"  frameborder="0"></iframe>
			</div>
		<div id="footer">
		</div>
	</body>
</html>