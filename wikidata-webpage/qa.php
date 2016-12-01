<!DOCTYPE HTML> 
<html>
	<head>
		<style>
			.error {color: #FF0000;}
		</style>
	</head>
<body> 

<?php

require "model/model.php";

$queryErr = $inputErr = "";
$query = $entity_name = $property_name = "";

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $query = "query1";
    switch ($query) {
        case 'query1':
            if (empty($_POST["query1-input1"]) or empty($_POST["query1-input2"])){
                $inputErr = "You have to input the query.";
            } else {
                $entity_name = test_input($_POST["query1-input1"]);
                $property_name = test_input($_POST["query1-input2"]);
            }
            break;
        default:
            echo "Fatal Error";
            die();
            break;
    } 
}

function test_input($data) {
   $data = trim($data);
   $data = stripslashes($data);
   $data = htmlspecialchars($data);
   return $data;
}
?>

<h2>Q&A system</h2>
<a href='index.php'>back to index</a><br><br>
<form method="post" action="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]);?>"> 

    What is the <input type="text" name="query1-input1"> of <input type="text" name="query1-input2"> 
    <br><br>

    <input type="submit" name="submit" value="submit"> 
</form>

<?php
if ($_SERVER["REQUEST_METHOD"] == "POST" and $inputErr == "" and $queryErr == "") {
    echo "<h2>Your query and input:</h2>";
    echo "query: ".$query;
    echo "<br>";
    echo "input1: ".$entity_name;
    echo "<br>";
    echo "input2: ".$property_name;
    switch ($query) {
        case 'query1':
            $base = qa_base($entity_name,$property_name);
            echo "<ul>";
            while($row = mysql_fetch_array($base)){
                $snak_value = mysql_fetch_array(qa_value($row["snak_id"], $row["datatype"]),MYSQL_ASSOC);
                if($snak_value){
                    echo "<li> ";
                    switch ($row["datatype"]) {
                        case 'globe-coordinate':
                            echo "latitude: ".$snak_value["latitude"]."<br>";
                            echo "longitude: ".$snak_value["longitude"]."<br>";
                            echo "altitude: ".$snak_value["altitude"]."<br>";
                            echo "precision: ".$snak_value["precision"]."<br>";
                            break;
                        case 'quantity':
                            echo "amount: ".$snak_value["amount"]."<br>";
                            echo "unit: ".$snak_value["unit"]."<br>";
                            break;
                        case 'string':
                            echo "value: ".$snak_value["value"]."<br>";
                            break;
                        case 'time':
                            echo "time: ".$snak_value["time"]."<br>";
                            echo "timezone: ".$snak_value["timezone"]."<br>";
                            echo "precision: ".$snak_value["precision"]."<br>";
                            echo "calendermodel: ".$snak_value["calendermodel"]."<br>";
                            break;
                        case 'wikibase-item':
                            echo "id: ".$snak_value["id"]."<br>";
                            break;
                        default:
                            break;
                    }
                }
                echo "</li>"."<br>";
            }
            echo "</ul>";
            break;
        default:
            echo "Fatal Error";
            die();
            break;
    }

    
} elseif ($_SERVER["REQUEST_METHOD"] == "POST") {
    if ($inputErr != "") {
        echo $inputErr."<br>";
    }
    if ($queryErr != "") {
        echo $queryErr."<br>";
    }
}
?>

</body>
</html>