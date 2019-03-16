package com.instigatemobile.linegraph;

import java.io.File;
import java.io.IOException;
import java.io.Reader;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;

import javafx.application.Application;
import javafx.event.ActionEvent;
import javax.imageio.ImageIO;
import javafx.stage.Stage;

import javafx.beans.binding.BooleanBinding;
import javafx.beans.property.ObjectProperty;
import javafx.beans.property.SimpleObjectProperty;

import static javafx.collections.FXCollections.observableArrayList;
import javafx.collections.ObservableList;
import javafx.embed.swing.SwingFXUtils;

import javafx.geometry.Insets;
import javafx.geometry.Point2D;
import javafx.geometry.Pos;

import javafx.scene.Node;
import javafx.scene.Scene;
import javafx.scene.chart.LineChart;
import javafx.scene.chart.NumberAxis;
import javafx.scene.chart.XYChart;
import javafx.scene.chart.XYChart.Series;
import javafx.scene.control.Button;
import javafx.scene.image.WritableImage;
import javafx.scene.input.MouseEvent;
import javafx.scene.layout.BorderPane;
import javafx.scene.layout.HBox;
import javafx.scene.layout.StackPane;
import javafx.scene.paint.Color;
import javafx.scene.shape.Rectangle;
import javafx.util.Pair;

import org.apache.commons.csv.CSVFormat;
import org.apache.commons.csv.CSVParser;
import org.apache.commons.csv.CSVRecord;


public class ZoomableLineGraph extends Application {
    private static String SAMPLE_CSV_FILE_PATH;
    private static String REPORT_IMAGE_PATH;
    private static Integer GRANULARITY;
    private static Double TPS_UPPER_BOUND = Double.MIN_VALUE;
    private static Double TPS_LOWER_BOUND = Double.MAX_VALUE;
    private static Double LATENCY_UPPER_BOUND = Double.MIN_VALUE;
    private static Double LATENCY_LOWER_BOUND = Double.MAX_VALUE;

    @Override
    public void start(Stage primaryStage) {
        // Get report file name
        Parameters params = getParameters();
        List<String> list = params.getRaw();
        SAMPLE_CSV_FILE_PATH = list.get(0);
        REPORT_IMAGE_PATH = list.get(1);
        GRANULARITY = Integer.parseInt(list.get(2));

        // Define and populate chart
        setBounds();
        final LineChart<Number, Number> chart = createChart();
        final StackPane chartContainer = new StackPane();
        chartContainer.getChildren().add(chart);

        // Define zoom rectangle
        final Rectangle zoomRect = new Rectangle();
        zoomRect.setManaged(false);
        zoomRect.setFill(Color.LIGHTSEAGREEN.deriveColor(0, 1, 1, 0.5));
        chartContainer.getChildren().add(zoomRect);

        setUpZooming(zoomRect, chart);
        final HBox controls = new HBox(10);
        controls.setPadding(new Insets(10));
        controls.setAlignment(Pos.CENTER);

        // Define application buttons
        final Button zoomButton = new Button("Zoom");
        final Button resetButton = new Button("Reset");

        // Assign functionality to zoom button
        zoomButton.setOnAction((ActionEvent event) -> {
            doZoom(zoomRect, chart);
        });

        // Assign functionality to reset button
        resetButton.setOnAction((ActionEvent event) -> {
            final NumberAxis xAxis = (NumberAxis)chart.getXAxis();
            xAxis.setLowerBound(TPS_LOWER_BOUND);
            xAxis.setUpperBound(TPS_UPPER_BOUND);
            final NumberAxis yAxis = (NumberAxis)chart.getYAxis();
            yAxis.setLowerBound(LATENCY_LOWER_BOUND);
            yAxis.setUpperBound(LATENCY_UPPER_BOUND);
            zoomRect.setWidth(0);
            zoomRect.setHeight(0);
        });

        // Set conditon to disable control buttons
        final BooleanBinding disableControls =
                zoomRect.widthProperty().lessThan(5)
                        .or(zoomRect.heightProperty().lessThan(5));
        zoomButton.disableProperty().bind(disableControls);
        controls.getChildren().addAll(zoomButton, resetButton);

        final BorderPane root = new BorderPane();
        root.setCenter(chartContainer);
        root.setBottom(controls);

        // Define scene and add chart to scene
        final Scene scene = new Scene(root, 1600, 1000);
        File f = new File("css/style.css");
        scene.getStylesheets().clear();
        scene.getStylesheets().add("file:///" + f.getAbsolutePath().replace("\\", "/"));

        // Export scene as png image
        export_to_png(scene);

        // Set title to stage
        primaryStage.setTitle("Latency / TPS curve");

        // Append scene to stage and show
        primaryStage.setScene(scene);
        primaryStage.show();
        primaryStage.hide();
    }


    private LineChart<Number, Number> createChart() {
        // Define X and Y axes
        final NumberAxis xAxis = createAxis(TPS_LOWER_BOUND, TPS_UPPER_BOUND);
        final NumberAxis yAxis = createAxis(LATENCY_LOWER_BOUND, LATENCY_UPPER_BOUND);
        xAxis.setLabel(String.format("Transactions Per %d Seconds", GRANULARITY));
        yAxis.setLabel("Average Latency");

        // Define chart, get series and append series to chart
        final LineChart<Number, Number> chart = new LineChart<>(xAxis, yAxis);
        chart.setTitle(String.format("Average Latency VS Transactions Per %d Seconds", GRANULARITY));

        Pair<ObservableList<Series<Number, Number>>, ArrayList<String>> data = generateChartData();
        chart.setData(data.getKey());

        // Add styles to series
        setStyles(data);

        chart.setLegendVisible(false);
        chart.setAnimated(false);
        return chart;
    }


    private NumberAxis createAxis(Double lowerBound, Double upperBound) {
        final NumberAxis axis = new NumberAxis();
        axis.setAutoRanging(false);
        axis.setUpperBound(upperBound);
        axis.setLowerBound(lowerBound);
        return axis;
    }


    private void setBounds() {
        try {
            Reader reader = Files.newBufferedReader(Paths.get(SAMPLE_CSV_FILE_PATH));
            CSVParser csvParser = new CSVParser(reader, CSVFormat.DEFAULT
                    .withFirstRecordAsHeader()
                    .withIgnoreHeaderCase()
                    .withTrim());

            Double tps;
            Double latency;
            for (CSVRecord csvRecord : csvParser) {
                // Get data from report file
                tps = Double.parseDouble(csvRecord.get("tps"));
                if (tps + tps / 50 > TPS_UPPER_BOUND) {
                    TPS_UPPER_BOUND = tps + tps / 50;
                }
                if (tps - tps / 50 < TPS_LOWER_BOUND) {
                    TPS_LOWER_BOUND = tps - tps / 50;
                }

                latency = Double.parseDouble(csvRecord.get("latency"));
                if (latency + latency / 50 > LATENCY_UPPER_BOUND) {
                    LATENCY_UPPER_BOUND = latency + latency / 50;
                }
                if (latency - latency  /50 < LATENCY_LOWER_BOUND) {
                    LATENCY_LOWER_BOUND = latency - latency / 50;
                }
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }


    private Pair<ObservableList<Series<Number, Number>>, ArrayList<String>> generateChartData() {
        // Define series container
        ArrayList<XYChart.Series<Number, Number>> seriesContainer = new ArrayList();
        ArrayList<String> labels = new ArrayList<>();
        try {
            // Read data from file
            Reader reader = Files.newBufferedReader(Paths.get(SAMPLE_CSV_FILE_PATH));
            CSVParser csvParser = new CSVParser(reader, CSVFormat.DEFAULT
                    .withFirstRecordAsHeader()
                    .withIgnoreHeaderCase()
                    .withTrim());

            Double tps = 0.0;
            Double latency = 0.0;
            String label;
            for (CSVRecord csvRecord : csvParser) {
                // Define a series
                XYChart.Series series = new XYChart.Series();

                // Populate the series with data
                if (tps != 0.0 && latency != 0.0) {
                    series.getData().add(new XYChart.Data(tps, latency));
                }

                // Get data from report file
                tps = Double.parseDouble(csvRecord.get("tps"));
                latency = Double.parseDouble(csvRecord.get("latency"));
                label = csvRecord.get("label");
                if (label.equals("failure")) {
                    if (latency == 0.0) {
                        label = "test_failure";
                    } else {
                        label = "statement_failure";
                    }
                }

                // Add data to series
                series.getData().add(new XYChart.Data(tps, latency));

                // Add series to series container
                seriesContainer.add(series);
                labels.add(label);
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
        return new Pair(observableArrayList((seriesContainer)), labels);
    }


    private void setStyles(Pair<ObservableList<Series<Number, Number>>, ArrayList<String>> data) {
        List<Series<Number, Number>> listOfSeries = data.getKey();
        ArrayList<String> labels = data.getValue();

        Integer size = labels.size();
        for (Integer i = 0; i < size; ++i) {
            XYChart.Series series = listOfSeries.get(i);

            // Add style class to series
            switch(labels.get(i)) {
                case "success":
                    setColor(series, "#42833d");
                    break;
                case "statement_failure":
                    setColor(series, "#fe8c3a");
                    break;
                case "test_failure":
                    setColor(series, "#bb2f21");
                    break;
            }
        }
    }


    private void setColor(XYChart.Series series, String color) {
        series.getNode().setStyle("-fx-stroke: " + color + ";");
    }


    private void setUpZooming(final Rectangle rect, final Node zoomingNode) {
        final ObjectProperty<Point2D> mouseAnchor = new SimpleObjectProperty<>();
        zoomingNode.setOnMousePressed((MouseEvent event) -> {
            mouseAnchor.set(new Point2D(event.getX(), event.getY()));
            rect.setWidth(0);
            rect.setHeight(0);
        });

        zoomingNode.setOnMouseDragged((MouseEvent event) -> {
            double x = event.getX();
            double y = event.getY();
            rect.setX(Math.min(x, mouseAnchor.get().getX()));
            rect.setY(Math.min(y, mouseAnchor.get().getY()));
            rect.setWidth(Math.abs(x - mouseAnchor.get().getX()));
            rect.setHeight(Math.abs(y - mouseAnchor.get().getY()));
        });
    }


    private void doZoom(Rectangle zoomRect, LineChart<Number, Number> chart) {
        Point2D zoomTopLeft = new Point2D(zoomRect.getX(), zoomRect.getY());
        Point2D zoomBottomRight = new Point2D(zoomRect.getX() + zoomRect.getWidth(), zoomRect.getY() + zoomRect.getHeight());

        final NumberAxis yAxis = (NumberAxis) chart.getYAxis();
        Point2D yAxisInScene = yAxis.localToScene(0, 0);

        final NumberAxis xAxis = (NumberAxis) chart.getXAxis();
        Point2D xAxisInScene = xAxis.localToScene(0, 0);

        double xOffset = zoomTopLeft.getX() - yAxisInScene.getX();
        double yOffset = zoomBottomRight.getY() - xAxisInScene.getY();
        double xAxisScale = xAxis.getScale();
        double yAxisScale = yAxis.getScale();

        xAxis.setLowerBound(xAxis.getLowerBound() + xOffset / xAxisScale);
        xAxis.setUpperBound(xAxis.getLowerBound() + zoomRect.getWidth() / xAxisScale);
        yAxis.setLowerBound(yAxis.getLowerBound() + yOffset / yAxisScale);
        yAxis.setUpperBound(yAxis.getLowerBound() - zoomRect.getHeight() / yAxisScale);

        zoomRect.setWidth(0);
        zoomRect.setHeight(0);
    }


    private void export_to_png(Scene scene) {
        // Export stage to png image file
        try {
            WritableImage snapShot = scene.snapshot(null);
            ImageIO.write(SwingFXUtils.fromFXImage(snapShot, null),
                          "png", new File(REPORT_IMAGE_PATH));
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public static void main(String[] args) {
        launch(args);
    }
}