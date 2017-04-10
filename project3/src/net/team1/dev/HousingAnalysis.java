//*** HousingAnalysis.java

package net.team1.dev;

import java.io.IOException;
import java.util.*;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

public class HousingAnalysis {

	    //**************************************************************************
	    public static class Map extends MapReduceBase implements Mapper<LongWritable, Text, Text, Text> {

	      //*** our variables are declared here
	      private Text key = new Text();
	      private Text variables = new Text();

	      public void map(LongWritable key, Text value, OutputCollector<Text, Text> output, Reporter reporter) throws IOException {

            //*** Housing data come in as lines of comma-separated data
	        String row[] = value.toString().split(",");

	        //Get the Variables 
			int count = 0;
			int rating = 0;
			
			int region = row[3];
			String location = row[75]; 
			int age = row[1]; 
			int persons = row[20];
			String ownRent = row[79];
			int income = row[32]; 
			
			//Normalize Location
			if(location.contains("-5"))
				location = "Suburban";
			else location = "City";   
			
			//Check for missing data 
			if(persons == -6)
				count = 0;
			else if(age == -9)
				count = 0;
			else if(ownRent.contains("."))
				count = 0;
			else if(income == -9)
				count = 0;
			else count = 1;
			
			if(count == 1) {
				rating = age%10 + persons; 
					if(ownRent.contains("own")) rating += 1;
					else rating += 2;
			}

	        key.set(region + "\t" + location);
			//Count[1 for all data available, 0for missing data]
			//  age, #persons, Own/Rent, Total Wage Income)
	        variables.set(count + "\t" + rating + "\t" + income); 

	        output.collect(key, variables);
	      }
	    }

		//**************************************************************************
	    public static class Reduce extends MapReduceBase implements Reducer<Text, Text, Text, Text> {
	      public void reduce(Text key, Iterator<Text> values, OutputCollector<Text, Text> output, Reporter reporter) throws IOException {

			int totalCount = 0;
			double ratingSum = 0;
			double incomeSum = 0;

	       while (values.hasNext()) {
			   String tokens[] = values.next().toString().split("\t");
			   int count = Integer.parseInt(tokens[0]);
			   int rating = Integer.parseInt(tokens[1]);
			   int income = Integer.parseInt(tokens[2]);

			   if (count == 1) {    // ignore houses with missing data
			        totalCount += count;
					ratingSum += rating;
					incomeSum += income; 
			   }
		   }

			output.collect(key, new Text( totalCount + "\t" + (rating/totalCount) + "\t" + (income/totalCount)));

	      }
	    }

		//**************************************************************************
	    public static void main(String[] args) throws Exception {
	      JobConf conf = new JobConf(HousingAnalysis.class);
	      conf.setJobName("housinganalysis");

	      conf.setOutputKeyClass(Text.class);
	      conf.setOutputValueClass(Text.class);

	      conf.setMapperClass(Map.class);
	      conf.setCombinerClass(Reduce.class);
	      conf.setReducerClass(Reduce.class);

	      conf.setInputFormat(TextInputFormat.class);
	      conf.setOutputFormat(TextOutputFormat.class);

	      FileInputFormat.setInputPaths(conf, new Path(args[0]));
	      FileOutputFormat.setOutputPath(conf, new Path(args[1]));

	      JobClient.runJob(conf);
	    }
}


