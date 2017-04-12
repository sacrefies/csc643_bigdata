// ----------------------------------------------------------------------------
// Copyright 2017 team1@course_bigdata, Saint Joseph's University
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
// ----------------------------------------------------------------------------

package net.team1.dev;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.FileStatus;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.fs.PathFilter;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapred.*;
import org.apache.hadoop.mapred.lib.MultipleInputs;

import java.io.IOException;
import java.util.HashMap;
import java.util.logging.Logger;


/**
 * A class for the map/reduce process
 */
public class HousingAnalysis {

    //**************************************************************************
    public static void main(String[] args) throws Exception {
        Path inputDir = new Path(args[0]);
        Path outputDir = new Path(args[1]);
        FileSystem fs = FileSystem.get(new Configuration());

        if (!fs.exists(inputDir))
            throw new IOException("The input path does not exist.");
        if (fs.isFile(inputDir))
            throw new IOException("The input path is a file.");
        if (fs.exists(outputDir)) fs.delete(outputDir, true);

        // set job configuration
        JobConf conf = new JobConf(HousingAnalysis.class);
        conf.setJobName("housinganalysis");
        conf.setOutputKeyClass(Text.class);
        conf.setOutputValueClass(Text.class);
        conf.setOutputFormat(TextOutputFormat.class);
        conf.setCombinerClass(HousingReducer.class);
        conf.setReducerClass(HousingReducer.class);

        // set multiple input files
        HashMap<Path, Class<? extends Mapper>> inputMappers = getInputFilePaths(inputDir, fs);
        for (Path p : inputMappers.keySet()) {
            MultipleInputs.addInputPath(conf, p, TextInputFormat.class, inputMappers.get(p));
            LOG.info(p.getName() + ": " + inputMappers.get(p).getName());
        }

        // set output
        FileOutputFormat.setOutputPath(conf, outputDir);

        // start the job
        JobClient.runJob(conf);
    }

    private static HashMap<Path, Class<? extends Mapper>> getInputFilePaths(Path inputDir, FileSystem fs) throws Exception {
        HashMap<Path, Class<? extends Mapper>> mappers = new HashMap<>();
        FileStatus files[] = fs.listStatus(inputDir, new PathFilter() {
            @Override
            public boolean accept(Path path) {
                String name = path.getName();
                return name.endsWith(".txt") && name.startsWith("thads");
            }
        });
        for (FileStatus f : files) {
            Path p = f.getPath();
            String fileName = p.getName();
            if (fileName.contains("2013"))
                mappers.put(p, Mapper2013.class);
            else if (fileName.contains("2003"))
                mappers.put(p, Mapper2003.class);
            else if (fileName.contains("2005"))
                mappers.put(p, Mapper2005.class);
            else if (fileName.contains("2007"))
                mappers.put(p, Mapper2007.class);
            else if (fileName.contains("2009"))
                mappers.put(p, Mapper2009.class);
            else if (fileName.contains("2011"))
                mappers.put(p, Mapper2011.class);
        }
        return mappers;
    }

    private static final Logger LOG = Logger.getLogger(HousingAnalysis.class.getName());
}


