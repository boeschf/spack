# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyTorchNvidiaApex(PythonPackage, CudaPackage):
    """A PyTorch Extension: Tools for easy mixed precision and
    distributed training in Pytorch"""

    homepage = "https://github.com/nvidia/apex/"
    git = "https://github.com/nvidia/apex/"

    license("BSD-3-Clause")

    version("master", branch="master")
    version("2020-10-19", commit="8a1ed9e8d35dfad26fb973996319965e4224dcdd")

    depends_on("python@3:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-packaging", type="build")
    depends_on("py-torch@0.4:", type=("build", "run"))
    depends_on("cuda@9:", when="+cuda")
    depends_on("py-pybind11", type=("build", "link", "run"))
    depends_on("ninja", type="build")
    # Required for using --config-settings (PEP 517 backend)
    depends_on("py-pip@23.1:", when="^python@3.11:", type="build")

    variant("cuda", default=False, description="Build with CUDA")
    variant("dist_adam", default=False, description="Build with distributed Adam optimizer")
    variant("dist_lamb", default=False, description="Build with distributed Lamb optimizer")
    variant("perm_search", default=False, description="Build with permutation search")
    variant("bnp", default=False, description="Build with batch norm")
    variant("xentropy", default=False, description="Build with cross entropy")
    variant("focal_loss", default=False, description="Build with focal loss")
    variant("group_norm", default=False, description="Build with group norm")
    variant("index_mul_2d", default=False, description="Build with index_mul_2d")
    variant("fast_layer_norm", default=False, description="Build with fast layer norm")
    variant("fmha", default=False, description="Build with fmha")
    variant("fast_multihead_attn", default=False, description="Build with fast multihead attn")
    variant("transducer", default=False, description="Build with transducer")
    variant("cudnn_gbn", default=False, description="Build with fast cudnn gbn")
    variant("peer_memory", default=False, description="Build with peer memory")
    variant("nccl_p2p", default=False, description="Build with nccl p2p")
    variant("fast_bottleneck", default=False, description="Build with fast_bottleneck")
    variant("fused_conv_bias_relu", default=False, description="Build with fused_conv_bias_relu")
    variant("gpu_direct_storage", default=False, description="Build with gpu_direct_storage")


    # https://github.com/NVIDIA/apex/issues/1498
    # https://github.com/NVIDIA/apex/pull/1499
    patch("1499.patch", when="@2020-10-19")

    def setup_build_environment(self, env):
        if "+cuda" in self.spec:
            env.set("CUDA_HOME", self.spec["cuda"].prefix)
        else:
            env.unset("CUDA_HOME")

    @when("^python@:3.10")
    def global_options(self, spec, prefix):
        args = []
        if spec.satisfies("^py-torch@1.0:"):
            args.append("--cpp_ext")
            if "+cuda" in spec:
                args.append("--cuda_ext")
            if "+dist_adam" in spec:
                args.append("--distributed_adam")
            if "+dist_lamb" in spec:
                args.append("--distributed_lamb")
            if "+perm_search" in spec:
                args.append("--permutation_search")
            if "+bnp" in spec:
                args.append("--bnp")
            if "+xentropy" in spec:
                args.append("--xentropy")
            if "+focal_loss" in spec:
                args.append("--focal_loss")
            if "+group_norm" in spec:
                args.append("--group_norm")
            if "+index_mul_2d" in spec:
                args.append("--index_mul_2d")
            if "+fast_layer_norm" in spec:
                args.append("--fast_layer_norm")
            if "+fmha" in spec:
                args.append("--fmha")
            if "+fast_multihead_attn" in spec:
                args.append("--fast_multihead_attn")
            if "+transducer" in spec:
                args.append("--transducer")
            if "+cudnn_gbn" in spec:
                args.append("--cudnn_gbn")
            if "+peer_memory" in spec:
                args.append("--peer_memory")
            if "+nccl_p2p" in spec:
                args.append("--nccl_p2p")
            if "+fast_bottleneck" in spec:
                args.append("--fast_bottleneck")
            if "+fused_conv_bias_relu" in spec:
                args.append("--fused_conv_bias_relu")
            if "+gpu_direct_storage" in spec:
                args.append("--gpu_direct_storage")
        return args

    @when("^python@3.11:")
    def config_settings(self, spec, prefix):
        build_opts = ""
        if spec.satisfies("^py-torch@1.0:"):
            build_opts += "--cpp_ext"
            if "+cuda" in spec:
                build_opts += " --cuda_ext"
            if "+dist_adam" in spec:
                build_opts += " --distributed_adam"
            if "+dist_lamb" in spec:
                build_opts += " --distributed_lamb"
            if "+perm_search" in spec:
                build_opts += " --permutation_search"
            if "+bnp" in spec:
                build_opts += " --bnp"
            if "+xentropy" in spec:
                build_opts += " --xentropy"
            if "+focal_loss" in spec:
                build_opts += " --focal_loss"
            if "+group_norm" in spec:
                build_opts += " --group_norm"
            if "+index_mul_2d" in spec:
                build_opts += " --index_mul_2d"
            if "+fast_layer_norm" in spec:
                build_opts += " --fast_layer_norm"
            if "+fmha" in spec:
                build_opts += " --fmha"
            if "+fast_multihead_attn" in spec:
                build_opts += " --fast_multihead_attn"
            if "+transducer" in spec:
                build_opts += " --transducer"
            if "+cudnn_gbn" in spec:
                build_opts += " --cudnn_gbn"
            if "+peer_memory" in spec:
                build_opts += " --peer_memory"
            if "+nccl_p2p" in spec:
                build_opts += " --nccl_p2p"
            if "+fast_bottleneck" in spec:
                build_opts += " --fast_bottleneck"
            if "+fused_conv_bias_relu" in spec:
                build_opts += " --fused_conv_bias_relu"
            if "+gpu_direct_storage" in spec:
                build_opts += " --gpu_direct_storage"
        return {
            "builddir": "build",
            "compile-args": f"-j{make_jobs}",
            "--global-option": build_opts,
        }
