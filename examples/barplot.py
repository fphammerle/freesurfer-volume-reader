import argparse

from matplotlib import pyplot
import pandas
import seaborn

from freesurfer_volume_reader.freesurfer import HippocampalSubfieldsVolumeFile
from freesurfer_volume_reader import read_hippocampal_volume_file_dataframe


def abbreviate_analysis_id(analysis_id):
    return analysis_id.split('_')[0] if analysis_id else None


def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument('--subject', required=True)
    argparser.add_argument('--subjects-dir', dest='subjects_dir_path', required=True)
    args = argparser.parse_args()
    volume_frame = pandas.concat(read_hippocampal_volume_file_dataframe(f)
                                 for f in HippocampalSubfieldsVolumeFile.find(args.subjects_dir_path))
    volume_frame = volume_frame[volume_frame['subject'] == args.subject]
    volume_frame['subfield_segmentation_mode'] = volume_frame.apply(
        lambda row: ' & '.join(filter(None, ('T1' if row['T1_input'] else None,
                                             abbreviate_analysis_id(row['analysis_id'])))),
        axis=1,
    )
    volume_frame.to_csv('hippocampal_subfield_volumes_{}.csv'.format(args.subject), index=False)
    volume_frame.drop(columns=['subject', 'T1_input', 'analysis_id'], inplace=True)
    print(volume_frame)
    volume_frame.sort_values(['subfield_segmentation_mode', 'subfield'], inplace=True)
    seaborn.set(font_scale=0.3)
    volume_frame_subfields = volume_frame[volume_frame['subfield'] != 'Whole_hippocampus']
    for hemisphere in ['left', 'right']:
        pyplot.ylim(0, 750)
        ax = seaborn.barplot(data=volume_frame_subfields[volume_frame_subfields['hemisphere'] == hemisphere],
                             x='subfield', y='volume_mm^3',
                             hue='subfield_segmentation_mode')
        ax.set_title('Hippocampal Subfield Volumes of Subject {}'.format(args.subject)
                     + '\n{} Hemisphere'.format(str.capitalize(hemisphere)))
        pyplot.savefig('hippocampal_subfield_volumes_{}_{}.png'.format(args.subject, hemisphere))
        pyplot.clf()
    seaborn.set(font_scale=0.4)
    ax = seaborn.barplot(data=volume_frame[volume_frame['subfield'] == 'Whole_hippocampus'],
                         x='hemisphere', y='volume_mm^3',
                         hue='subfield_segmentation_mode')
    ax.set_title('Hippocampal Volume of Subject {}'.format(args.subject))
    pyplot.savefig('hippocampal_volume_{}.png'.format(args.subject))


if __name__ == '__main__':
    main()
