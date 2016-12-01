<!DOCTYPE HTML> 
<html>
	<head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
		<style>
			.error {color: #FF0000;}
		</style>
	</head>
<body> 

<?php

require "model/model.php";

$queryErr = $inputErr = "";
$query = $input = "";
$lan="en";

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $lan=test_input($_POST["lan"]);
    if (empty($_POST["query-check"])) {
        $queryErr = "You have to select exactly one query.";
    } else {
        $query = test_input($_POST["query-check"]);
        switch ($query) {
            case 'query1':
                if (empty($_POST["query1-input"])){
                    $inputErr = "You have to input the query.";
                } else {
                    $input = test_input($_POST["query1-input"]);
                }
                break;
            case 'query2':
                if (empty($_POST["query2-input"])){
                    $inputErr = "You have to input the query.";
                } else {
                    $input = test_input($_POST["query2-input"]);
                }
                break;
            case 'query3':
                if (empty($_POST["query3-input"])){
                    $inputErr = "You have to input the query.";
                } else {
                    $input = test_input($_POST["query3-input"]);
                }
                break;
            case 'query4':
                if (empty($_POST["query4-input"])){
                    $inputErr = "You have to input the query.";
                } else {
                    $input = test_input($_POST["query4-input"]);
                }
                break;
            default:
                echo "Fatal Error";
                die();
                break;
        }
    } 
}

function test_input($data) {
   $data = trim($data);
   $data = stripslashes($data);
   $data = htmlspecialchars($data);
   return $data;
}
?>

<h2>Queries</h2>
<form method="post" action="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]);?>"> 
    language: 
    <select name="lan">
        <?php
            $res=all_language();
            echo "<option value='en'>en</option>";
            while($row = mysql_fetch_array($res)){
                    echo "<option value='".$row["entity_language"]."'>";
                    echo $row["entity_language"]."</option>";
                }
        ?>
    </select>
    <br><br>

    <input type="radio" name="query-check" value="query1">Query 1<br>
    Given a name, return all the entities that match the name.
    <br><input type="text" name="query1-input">
    <br><br>

    <input type="radio" name="query-check" value="query2">Query 2<br>
    Given an entity, return all preceeding categories.
    <br><input type="text" name="query2-input"> 
    <br><br>

    <input type="radio" name="query-check" value="query3">Query 3<br>
    Given an entity, return all entities that are co-occurred with this eneity in one statement.
    <br><input type="text" name="query3-input"> 
    <br><br>

    <input type="radio" name="query-check" value="query4">Query 4<br>
    Given an entity, return all the properties and statements it posesses.
    <br><input type="text" name="query4-input"> 
    <br><br>

    <input type="submit" name="submit" value="submit"> 
</form>

<?php
if ($_SERVER["REQUEST_METHOD"] == "POST" and $inputErr == "" and $queryErr == "") {
    echo "<h2>Your query and input:</h2>";
    echo "query: ".$query;
    echo "<br>";
    echo "input: ".$input;
    echo "<br>";
    echo "language: ".$lan;
    echo "<br>";
    echo "result: <br>";
    switch ($query) {
        case 'query1':
            if (empty($_POST["query1-input"])){
                $inputErr = "You have to input the query.";
            } else {
                $input = test_input($_POST["query1-input"]);
                $result = query1($input, $lan);
                echo "<ul>";
                while($row = mysql_fetch_array($result)){
                    echo "<li>";
                    echo "entity name: ".$row["entity_text"]."<br>";
                    echo "entity description: ".$row["desc_text"]."<br>";
                    echo "entity id: ".$row["entity_id"]."</li>"."<br>";
                }
                echo "</ul>";
            }
            break;
        case 'query2':
            if (empty($_POST["query2-input"])){
                $inputErr = "You have to input the query.";
            } else {
                $input = test_input($_POST["query2-input"]);
                $result = query2($input,$lan);
                echo "<ul>";
                while($row = mysql_fetch_array($result)){
                    echo "<li>";
                    echo "category name: ".$row["entity_text"]."<br>";
                    echo "category id: ".$row["entity_id"]."</li>"."<br>";
                }
                echo "</ul>";
            }
            break;
        case 'query3':
            if (empty($_POST["query3-input"])){
                $inputErr = "You have to input the query.";
            } else {
                $input = test_input($_POST["query3-input"]);
                $result = query3($input);
                echo "<ul>";
                while($row = mysql_fetch_array($result)){
                    $result_name = mysql_fetch_array(entity_text_by_id($row["result_id"],$lan));
                    echo "<li> entity_name: ".$result_name["entity_text"]."<br>";
                    echo "entity_id: ".$row["result_id"]."<br>";
                    echo "query_id: ".$row["query_id"]."</li>"."<br>";
                }
                echo "</ul>";
            }
            break;
        case 'query4':
            if (empty($_POST["query4-input"])){
                $inputErr = "You have to input the query.";
            } else {
                $input = test_input($_POST["query4-input"]);
                $result1 = query4_properties($input,$lan);
                $result2 = query4_statements($input,$lan);
                echo "<ul>";
                while($row = mysql_fetch_array($result1)){
                    echo "<li>";
                    echo "property id: ".$row["property_id"]."<br>";
                    echo "property name: ".$row["property_text"]."<br>";
                    echo "property description: ".$row["property_desc_text"]."<br>";
                    echo "queried entity id: ".$row["entity_id"]."<br>";
                    echo "queried entity name: ".$row["entity_text"]."<br>";
                    echo "queried entity description: ".$row["desc_text"]."</li>"."<br>";
                }
                while($row = mysql_fetch_array($result2)){
                    echo "<li>";
                    echo "statements id: ".$row["snak_id"]."<br>";
                    echo "queried entity id: ".$row["entity_id"]."<br>";
                    echo "queried entity name: ".$row["entity_text"]."<br>";
                    echo "queried entity description: ".$row["desc_text"]."</li>"."<br>";
                }
                echo "</ul>";
            }
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