# Speech to Text with OpenAI Whisper-1 Model and GPT-4o for Post Processing (Version 3.1)

# Upcoming Version 4 (ToDo):
1. Add a easy to use GUI
2. Add a requirement.txt

This project provides scripts for recording and transcribing long academic research presentations.

## What Does It Do?

1. Records audio from Zoom or a microphone and generates transcripts using the Whisper-1 model.
2. Post-processes the transcription with GPT-4. The context of the recorded audio, including the research title, abstract, and presenter's name, is needed.

## Notes

1. The scripts are built and tested on macOS.
2. An OpenAI API key is required (for Version 3; Versions 1 and 2 do not utilize OpenAI models).
3. You need to download SoundFlower and configure the multi-audio output.
4. Remember to make `run.command` executable with `chmod +x run.command`.

## Usage

1. Configure the OpenAI API key according to [this guide](https://platform.openai.com/docs/quickstart).
2. Install and configure SoundFlower.
3. Configure multi-audio output, ensuring SoundFlower is one of the output devices (SoundFlower reroutes output back to input so that system sound can be recorded).
4. Make `run.command` executable with `chmod +x run.command`.
5. Run the `run.command` file (`./run.command`). This will launch the recorder and transcriber. The recorder will record for 60 seconds and save a `.wav` file in the `./segments` directory while sending the audio file to OpenAI Whisper-1 for transcription. The resulting transcript will be stored in `transcription.txt`.
6. Stop the recording after the transcription is fully obtained. Rename `transcription.txt` to `presenter_name.txt`.
7. In `parallel_GPT4o_postprocessing.py`, add metadata of the presentation to the `presentation_info_object` under the `__main__` part of the program.
8. Execute `parallel_GPT4o_postprocessing.py`. The post-processed transcription will be stored in the `./processed_transcriptions` directory.

***

# OpenAI Whisper-1 モデルを使用した文字起こしとGPT-4oを使用した後処理 (Version 3.1)

このプロジェクトは、学術研究プレゼンテーションを録音し、文字起こしを行うためのスクリプトを提供します。

## 機能

1. Zoomやマイクからの音声を録音し、Whisper-1モデルを使用して文字起こしを生成します。
2. 録音した音声の文脈（研究タイトル、研究概要、発表者の名前）を含む文字起こしをGPT-4で後処理します。

## 注意事項

1. スクリプトはmacOSで構築およびテストされています。
2. OpenAI APIキーが必要です（バージョン3の場合。バージョン1と2ではOpenAIモデルを使用しません）。
3. SoundFlowerをダウンロードし、マルチオーディオ出力を設定する必要があります。
4. `run.command`を実行可能にするには、`chmod +x run.command`を実行してください。

## 使用方法

1. [このガイド](https://platform.openai.com/docs/quickstart)に従ってOpenAI APIキーを設定します。
2. SoundFlowerをインストールし、設定します。
3. マルチオーディオ出力を設定し、SoundFlowerが出力デバイスの1つであることを確認します（SoundFlowerは出力を入力にリルートするため、システム音が録音されます）。
4. `run.command`を実行可能にします（`chmod +x run.command`）。
5. `run.command`ファイルを実行します（`./run.command`）。これにより、レコーダーとトランスクリプタが起動します。レコーダーは60秒間録音し、`./segments`ディレクトリに.wavファイルを保存し、音声ファイルをOpenAI Whisper-1に送信して文字起こしを行います。結果の文字起こしは`transcription.txt`に保存されます。
6. 文字起こしが完全に取得されたら録音を停止します。`transcription.txt`を`presenter_name.txt`にリネームします。
7. `parallel_GPT4o_postprocessing.py`内で、プレゼンテーションのメタデータをプログラムの`__main__`部分にある`presentation_info_object`に追加します。
8. `parallel_GPT4o_postprocessing.py`を実行します。後処理された文字起こしは`./processed_transcriptions`ディレクトリに保存されます。

***

# 使用 OpenAI Whisper-1 模型进行语音转文本与使用GPT-4o进行文本的后续处理 (Version 3.1)

该项目提供了用于录制和转录长时间的学术研究演讲的脚本。

## 功能简介

1. 录制来自 Zoom 或麦克风的音频，并使用 Whisper-1 模型生成转录文本。
2. 使用 GPT-4 对转录文本进行后处理。需要提供录制音频的上下文信息，包括研究标题、研究摘要和演讲者姓名。

## 注意事项

1. 脚本在 macOS 上构建和测试。
2. 需要 OpenAI API 密钥（适用于版本3；版本1和2不使用 OpenAI 模型）。
3. 需要下载 SoundFlower 并配置多音频输出。
4. 请记得通过 `chmod +x run.command` 使 `run.command` 具有可执行权限。

## 使用方法

1. 根据[此指南](https://platform.openai.com/docs/quickstart)配置 OpenAI API 密钥。
2. 安装并配置 SoundFlower。
3. 配置多音频输出，确保 SoundFlower 是输出设备之一（SoundFlower 将输出重定向到输入，以便系统声音可以被录制）。
4. 使 `run.command` 可执行（`chmod +x run.command`）。
5. 运行 `run.command` 文件（`./run.command`）。这将启动录音和转录程序，录音机会录制60秒并将 .wav 文件保存到 `./segments` 目录，同时将音频文件发送到 OpenAI Whisper-1 进行转录。转录结果将存储在 `transcription.txt` 中。
6. 在完全获得转录文本后停止录音。将 `transcription.txt` 重命名为 `presenter_name.txt`。
7. 在 `parallel_GPT4o_postprocessing.py` 中，在程序的 `__main__` 部分，将演示文稿的元数据添加到 `presentation_info_object` 对象中。
8. 执行 `parallel_GPT4o_postprocessing.py`，后处理后的转录文本将存储在 `./processed_transcriptions` 目录中。
