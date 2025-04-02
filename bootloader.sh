#!/bin/bash

set -e

# 检查命令行参数
if [ $# -ne 2 ]; then
  echo "用法：$0 <boot分区路径> <根分区设备名>"
  echo "例如：$0 /boot /dev/sda2"
  exit 1
fi

boot_path="$1"
root_partition="$2"

# 1. 安装 systemd-boot
echo "1. 安装 systemd-boot..."
bootctl --path="$boot_path" install
if [ $? -ne 0 ]; then
  echo "错误：安装 systemd-boot 失败。"
  exit 1
fi
echo "systemd-boot 安装完成。"

# 2. 配置 loader.conf
echo "2. 配置 loader.conf..."
loader_conf="$boot_path/loader/loader.conf"
cat << EOF > "$loader_conf"
default arch.conf
timeout 4
console-mode max
editor no
EOF
if [ $? -ne 0 ]; then
  echo "错误：配置 loader.conf 失败。"
  exit 1
fi
echo "loader.conf 配置完成。"

# 3. 获取根分区 UUID
echo "3. 获取根分区 UUID..."
uuid=$(blkid "$root_partition" | awk -F '"' '{print $2}')
if [ -z "$uuid" ]; then
  echo "错误：获取根分区 UUID 失败。"
  exit 1
fi
echo "根分区 UUID：$uuid"

# 4. 创建 arch.conf 启动项
echo "4. 创建 arch.conf 启动项..."
arch_conf="$boot_path/loader/entries/arch.conf"
cat << EOF > "$arch_conf"
title GNU/Linux Arch
linux /vmlinuz-linux
initrd /intel-ucode.img
initrd /initramfs-linux.img
options root=UUID=$uuid rootflags=subvol=@ rw
EOF
if [ $? -ne 0 ]; then
  echo "错误：创建 arch.conf 启动项失败。"
  exit 1
fi
echo "arch.conf 启动项创建完成。"

echo "systemd-boot 配置完成！"
