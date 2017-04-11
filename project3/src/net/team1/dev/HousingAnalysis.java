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

import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapred.*;
import java.util.logging.Logger;


/**
 * A class for the map/reduce process
 */
public class HousingAnalysis {

    private static final Logger LOG = Logger.getLogger(HousingAnalysis.class.getName());

    //**************************************************************************
    public static void main(String[] args) throws Exception {
        LOG.info(args[0]);
        LOG.info(args[1]);
        JobConf conf = new JobConf(HousingAnalysis.class);
        conf.setJobName("housinganalysis");

        conf.setOutputKeyClass(Text.class);
        conf.setOutputValueClass(Text.class);

        conf.setMapperClass(Mapper2013.class);
        conf.setCombinerClass(HousingReducer.class);
        conf.setReducerClass(HousingReducer.class);

        conf.setInputFormat(TextInputFormat.class);
        conf.setOutputFormat(TextOutputFormat.class);

        FileInputFormat.setInputPaths(conf, new Path(args[0]));
        FileOutputFormat.setOutputPath(conf, new Path(args[1]));

        JobClient.runJob(conf);
    }
}


